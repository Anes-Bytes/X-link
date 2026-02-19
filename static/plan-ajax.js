document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.ajax-toggle');
    const container = document.getElementById('pricing-cards-container');

    if (toggleButtons.length && container) {
        toggleButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const period = this.getAttribute('data-period');
                const url = new URL(window.location.href);
                url.searchParams.set('period', period);

                // Add loading state
                container.style.opacity = '0.5';
                container.style.pointerEvents = 'none';

                // Update active state of buttons and indicator
                toggleButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const toggleContainer = this.closest('.period-toggle');
                if (toggleContainer) {
                    toggleContainer.setAttribute('data-active', period);
                }

                fetch(url.toString(), {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.text())
                .then(html => {
                    container.innerHTML = html;
                    
                    // Reset state
                    container.style.opacity = '1';
                    container.style.pointerEvents = 'auto';
                    
                    // Optional: Update URL without refresh
                    window.history.pushState({}, '', url.toString());
                })
                .catch(error => {
                    console.error('Error fetching plans:', error);
                    container.style.opacity = '1';
                    container.style.pointerEvents = 'auto';
                });
            });
        });
    }
});
