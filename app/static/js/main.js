// Main JavaScript for Diary App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations for entry cards
    initCardAnimations();
    
    // Auto-hide alerts after 5 seconds with fade animation
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 300);
        }, 5000);
    });

    // Image preview for file uploads
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const previewContainer = document.getElementById('imagePreview');
            
            if (previewContainer) {
                previewContainer.innerHTML = '';
                
                Array.from(files).forEach((file, index) => {
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const preview = document.createElement('div');
                            preview.className = 'image-upload-preview fade-in';
                            preview.innerHTML = `
                                <img src="${e.target.result}" alt="Preview ${index + 1}">
                            `;
                            previewContainer.appendChild(preview);
                        };
                        reader.readAsDataURL(file);
                    }
                });
            }
        });
    });

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'form-text text-end';
            counter.textContent = `0 / ${maxLength} characters`;
            textarea.parentNode.appendChild(counter);

            textarea.addEventListener('input', function() {
                const length = this.value.length;
                counter.textContent = `${length} / ${maxLength} characters`;
                if (length > maxLength * 0.9) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            });
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Initialize FAB tooltip
    const fabBtn = document.querySelector('.fab-btn');
    if (fabBtn) {
        fabBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(90deg)';
        });
        fabBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    }
});

// Initialize staggered card animations
function initCardAnimations() {
    const cards = document.querySelectorAll('.entry-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${0.1 + (index * 0.05)}s`;
        
        // Trigger animation when in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(card);
    });
}

// Utility functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    const bgMap = {
        'success': 'toast-success',
        'error': 'toast-error',
        'warning': 'bg-warning',
        'info': 'bg-primary'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white ${bgMap[type] || 'bg-primary'} border-0 fade-in`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${iconMap[type] || 'fa-info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 4000 });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Export for use in other scripts
window.DiaryApp = {
    showToast,
    formatDate
};
