const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const { exec } = require('child_process');
const util = require('util');
const Queue = require('bull');

const execPromise = util.promisify(exec);
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 20 * 1024 * 1024 } // 20MB limit
});

// Initialize Bull queue
const pdfConversionQueue = new Queue('pdf-conversion', {
  redis: { host: 'localhost', port: 6379 }
});

// GET PDF to Word converter form
router.get('/pdf-to-word', (req, res) => {
  res.render('./tools/pdf/pdf-to-word', { error: null, result: null });
});

// POST convert PDF to Word
router.post('/pdf-to-word', upload.single('pdfFile'), async (req, res) => {
  if (!req.file) {
    return res.render('./tools/pdf/pdf-to-word', {
      error: 'Please upload a PDF file.',
      result: null
    });
  }

  if (path.extname(req.file.originalname).toLowerCase() !== '.pdf') {
    return res.render('./tools/pdf/pdf-to-word', {
      error: 'Only PDF files are allowed.',
      result: null
    });
  }

  // Add job to the queue
  const job = await pdfConversionQueue.add({
    fileBuffer: req.file.buffer,
    originalFilename: req.file.originalname
  });

  res.render('./tools/pdf/pdf-to-word', {
    error: null,
    result: {
      message: 'Your file is queued for conversion.',
      jobId: job.id
    }
  });
});

// Process jobs in the queue
pdfConversionQueue.process(async (job, done) => {
  const { fileBuffer, originalFilename } = job.data;
  let tempDir = '/var/www/temp_pdf2word';
  let pdfPath, docxPath;

  try {
    // Create temporary directory
    try {
      await fs.mkdir(tempDir, { recursive: true });
      await fs.access(tempDir, fs.constants.W_OK);
    } catch (err) {
      console.warn(`Failed to use ${tempDir}: ${err.message}. Falling back to /tmp/pdf2word_temp`);
      tempDir = '/tmp/pdf2word_temp';
      await fs.mkdir(tempDir, { recursive: true });
    }

    // Save uploaded PDF to temporary file
    const timestamp = Date.now();
    pdfPath = path.join(tempDir, `input-${timestamp}.pdf`);
    docxPath = path.join(tempDir, `output-${timestamp}.docx`);
    await fs.writeFile(pdfPath, fileBuffer);

    // Path to Python script
    const pythonScript = path.join(__dirname, '../../public/js/convert_pdf_to_docx.py');

    // Use virtual environment's Python binary
    const conversionCmd = `/var/www/venv/bin/python "${pythonScript}" "${pdfPath}" "${docxPath}"`;
    const { stdout, stderr } = await execPromise(conversionCmd, { timeout: 120000 }); // Increased to 120s

    console.log('Python stdout:', stdout);
    if (stderr) console.warn('Python stderr:', stderr);

    if (!stdout.includes('success')) {
      throw new Error(`PDF to DOCX conversion failed. Details: ${stdout || stderr}`);
    }

    // Check if DOCX exists
    try {
      await fs.access(docxPath);
    } catch (err) {
      throw new Error(`Python conversion failed: Output DOCX file not found.`);
    }

    const wordBuffer = await fs.readFile(docxPath);
    const base64Word = wordBuffer.toString('base64');
    const wordFilename = originalFilename.replace(/\.pdf$/i, '.docx'); // Safer regex

    console.log(`Job ${job.id} completed for ${wordFilename}`);

    done(null, {
      originalFilename,
      wordFilename,
      base64Word,
      textLength: wordBuffer.length,
      pageCount: 1,
      isScanned: stdout.includes('OCR') // Optional: Indicate if OCR was used
    });

  } catch (err) {
    console.error(`Job ${job.id} failed:`, err);
    let errorMessage = err.message;
    if (errorMessage.includes('Password-protected')) {
      errorMessage = 'Password-protected PDFs are not supported.';
    } else if (errorMessage.includes('timeout')) {
      errorMessage = 'Conversion timed out. The PDF may be too large or complex.';
    }
    done(new Error(errorMessage));
  } finally {
    try {
      await fs.rm(tempDir, { recursive: true, force: true });
    } catch (cleanupErr) {
      console.warn('Failed to clean up temporary files:', cleanupErr);
    }
  }
});

// Endpoint to check job status
router.get('/pdf-to-word/status/:jobId', async (req, res) => {
  const jobId = req.params.jobId;
  const job = await pdfConversionQueue.getJob(jobId);

  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }

  const state = await job.getState();
  if (state === 'completed') {
    const result = job.returnvalue;
    if (result) {
      return res.render('./tools/pdf/pdf-to-word', {
        error: null,
        result
      });
    }
    return res.status(500).json({ error: 'Job completed but no result found' });
  } else if (state === 'failed') {
    return res.render('./tools/pdf/pdf-to-word', {
      error: `Conversion failed: ${job.failedReason}`,
      result: null
    });
  } else {
    return res.json({ status: state, message: 'Job is still processing or queued' });
  }
});

module.exports = router;