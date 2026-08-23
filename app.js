document.addEventListener('DOMContentLoaded', () => {
    // --- Header Scrolled Shadow & Height ---
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    });

    // --- Mobile Menu Toggle ---
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('open');
        navLinks.classList.toggle('open');
    });

    // Close menu when a link is clicked
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('open');
            navLinks.classList.remove('open');
        });
    });

    // --- Active Link Highlight on Scroll ---
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-links a');

    function highlightNavigation() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
            const sectionId = current.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href') === `#${sectionId}`) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }
    window.addEventListener('scroll', highlightNavigation);

    // --- Scroll Reveal Animations ---
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target); // Reveal once
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(element => {
        revealObserver.observe(element);
    });

    // --- Interactive FastAPI Terminal ---
    const terminalTabs = document.querySelectorAll('.terminal-tab');
    const terminalCmd = document.querySelector('.terminal-prompt .cmd');
    const terminalOutput = document.querySelector('.terminal-output');

    const apiEndpoints = {
        health: {
            cmd: 'curl -X GET "/api/v1/health"',
            response: `{
  <span class="json-key">"status"</span>: <span class="json-val">"healthy"</span>,
  <span class="json-key">"version"</span>: <span class="json-val">"1.0.0"</span>,
  <span class="json-key">"uptime"</span>: <span class="json-val">"348210s"</span>,
  <span class="json-key">"services"</span>: {
    <span class="json-key">"database"</span>: <span class="json-val">"connected"</span>,
    <span class="json-key">"storage"</span>: <span class="json-val">"active"</span>,
    <span class="json-key">"auth_provider"</span>: <span class="json-val">"operational"</span>
  }
}`
        },
        profile: {
            cmd: 'curl -X GET "/api/v1/developer/profile"',
            response: `{
  <span class="json-key">"name"</span>: <span class="json-val">"Madhura Surve"</span>,
  <span class="json-key">"headline"</span>: <span class="json-val">"Python Backend Developer & AI Enthusiast"</span>,
  <span class="json-key">"education"</span>: {
    <span class="json-key">"degree"</span>: <span class="json-val">"BCA Student"</span>,
    <span class="json-key">"focus"</span>: <span class="json-val">"Computer Applications & Backend Engineering"</span>
  },
  <span class="json-key">"status"</span>: <span class="json-val">"open_to_freelance_and_full_time"</span>,
  <span class="json-key">"core_stack"</span>: [
    <span class="json-val">"Python"</span>,
    <span class="json-val">"FastAPI"</span>,
    <span class="json-val">"PostgreSQL"</span>,
    <span class="json-val">"Supabase"</span>,
    <span class="json-val">"React"</span>
  ]
}`
        },
        sevasetu: {
            cmd: 'curl -X GET "/api/v1/projects/seva-setu"',
            response: `{
  <span class="json-key">"title"</span>: <span class="json-val">"Seva Setu"</span>,
  <span class="json-key">"type"</span>: <span class="json-val">"Digital Civic Complaint Management"</span>,
  <span class="json-key">"stack"</span>: {
    <span class="json-key">"backend"</span>: [<span class="json-val">"FastAPI"</span>, <span class="json-val">"Python"</span>],
    <span class="json-key">"database"</span>: [<span class="json-val">"PostgreSQL"</span>, <span class="json-val">"Supabase"</span>],
    <span class="json-key">"frontend"</span>: [<span class="json-val">"React Native"</span>, <span class="json-val">"Expo"</span>, <span class="json-val">"TypeScript"</span>]
  },
  <span class="json-key">"features"</span>: [
    <span class="json-val">"JWT Auth"</span>,
    <span class="json-val">"Complaint Tracking"</span>,
    <span class="json-val">"Photo Uploads"</span>,
    <span class="json-val">"Official Dashboard"</span>
  ]
}`
        },
        airbnb: {
            cmd: 'curl -X GET "/api/v1/projects/airbnb-clone"',
            response: `{
  <span class="json-key">"title"</span>: <span class="json-val">"Airbnb Clone"</span>,
  <span class="json-key">"type"</span>: <span class="json-val">"Full-Stack Property Booking"</span>,
  <span class="json-key">"stack"</span>: {
    <span class="json-key">"frontend"</span>: [<span class="json-val">"React"</span>],
    <span class="json-key">"backend"</span>: [<span class="json-val">"Node.js"</span>, <span class="json-val">"Express.js"</span>],
    <span class="json-key">"database"</span>: [<span class="json-val">"MongoDB"</span>]
  },
  <span class="json-key">"authentication"</span>: <span class="json-val">"Session-based"</span>,
  <span class="json-key">"database_driven_flows"</span>: <span class="json-bool">true</span>
}`
        }
    };

    function loadTerminalEndpoint(endpointKey) {
        const data = apiEndpoints[endpointKey];
        if (!data) return;

        // Clear output
        terminalOutput.innerHTML = '';
        terminalCmd.textContent = '';
        
        // Type effect for cmd
        let index = 0;
        const cmdText = data.cmd;
        
        function typeCmd() {
            if (index < cmdText.length) {
                terminalCmd.textContent += cmdText.charAt(index);
                index++;
                setTimeout(typeCmd, 15);
            } else {
                // Show output instantly after command typing is done
                setTimeout(() => {
                    terminalOutput.innerHTML = data.response;
                }, 100);
            }
        }
        
        typeCmd();
    }

    terminalTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            terminalTabs.forEach(t => t.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            const endpoint = e.currentTarget.dataset.endpoint;
            loadTerminalEndpoint(endpoint);
        });
    });

    // Load default endpoint
    loadTerminalEndpoint('health');

    // --- Contact Form Handling ---
    const contactForm = document.getElementById('contactForm');
    const formStatus = document.getElementById('formStatus');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !message) {
                formStatus.className = 'form-status error';
                formStatus.textContent = 'Please fill out all fields.';
                return;
            }

            // Simple Email format check
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                formStatus.className = 'form-status error';
                formStatus.textContent = 'Please enter a valid email address.';
                return;
            }

            // Simulate form submission
            formStatus.className = 'form-status success';
            formStatus.textContent = 'Thank you for reaching out! I will get back to you as soon as possible.';
            
            // Clear fields
            contactForm.reset();
        });
    }
});
