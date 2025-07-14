// JavaScript for the PDF to Word Converter landing page

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add active class to nav links based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Add animation to feature cards on scroll
    const featureCards = document.querySelectorAll('.feature-card');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.1 });
    
    featureCards.forEach(card => {
        observer.observe(card);
    });
    
    // Add countdown for redirect
    const redirectTime = 5; // seconds
    let timeLeft = redirectTime;
    
    // Create countdown element
    const countdownContainer = document.createElement('div');
    countdownContainer.style.position = 'fixed';
    countdownContainer.style.bottom = '20px';
    countdownContainer.style.right = '20px';
    countdownContainer.style.backgroundColor = 'rgba(30, 136, 229, 0.9)';
    countdownContainer.style.color = 'white';
    countdownContainer.style.padding = '10px 20px';
    countdownContainer.style.borderRadius = '5px';
    countdownContainer.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
    countdownContainer.style.zIndex = '1000';
    countdownContainer.style.display = 'flex';
    countdownContainer.style.alignItems = 'center';
    countdownContainer.style.gap = '10px';
    
    const countdownText = document.createElement('span');
    countdownText.textContent = `Redirecting to app in ${timeLeft} seconds...`;
    
    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancel';
    cancelButton.style.backgroundColor = 'white';
    cancelButton.style.color = '#1E88E5';
    cancelButton.style.border = 'none';
    cancelButton.style.padding = '5px 10px';
    cancelButton.style.borderRadius = '3px';
    cancelButton.style.cursor = 'pointer';
    
    countdownContainer.appendChild(countdownText);
    countdownContainer.appendChild(cancelButton);
    document.body.appendChild(countdownContainer);
    
    // Update countdown
    const countdownInterval = setInterval(() => {
        timeLeft--;
        countdownText.textContent = `Redirecting to app in ${timeLeft} seconds...`;
        
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            window.location.href = 'https://share.streamlit.io/yourusername/pdf-to-word-converter/main/app.py';
        }
    }, 1000);
    
    // Cancel redirect
    cancelButton.addEventListener('click', () => {
        clearInterval(countdownInterval);
        countdownContainer.remove();
    });
});