
document.addEventListener('DOMContentLoaded', function () {

    console.log('MarvelSpace Comic Universe initialized');

    // Comic animations

    const animatedElements = document.querySelectorAll('.comic-animate');

    animatedElements.forEach(function (element, index) {
        element.style.animationDelay = `${index * 0.08}s`;
    });


    // Post carousels

    const carousels = document.querySelectorAll('[data-carousel]');

    carousels.forEach(function (carousel) {

        const slides = carousel.querySelectorAll('.post-carousel-slide');
        const dots = carousel.querySelectorAll('.carousel-dot');
        const previousButton = carousel.querySelector('[data-carousel-prev]');
        const nextButton = carousel.querySelector('[data-carousel-next]');
        const counter = carousel.querySelector('[data-carousel-current]');

        if (slides.length === 0) {
            return;
        }

        let currentIndex = 0;
        let startX = 0;
        let startY = 0;
        let isSwiping = false;

        function showSlide(index) {

            if (index < 0) {
                index = slides.length - 1;
            }

            if (index >= slides.length) {
                index = 0;
            }

            currentIndex = index;

            slides.forEach(function (slide, slideIndex) {

                const isActive = slideIndex === currentIndex;

                slide.classList.toggle('active', isActive);

                const video = slide.querySelector('video');

                if (video && !isActive) {
                    video.pause();
                }
            });

            dots.forEach(function (dot, dotIndex) {
                dot.classList.toggle('active', dotIndex === currentIndex);
            });

            if (counter) {
                counter.textContent = currentIndex + 1;
            }
        }


        // Previous and next buttons

        if (previousButton) {
            previousButton.addEventListener('click', function () {
                showSlide(currentIndex - 1);
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', function () {
                showSlide(currentIndex + 1);
            });
        }


        // Indicator buttons

        dots.forEach(function (dot) {

            dot.addEventListener('click', function () {

                const index = Number(dot.dataset.carouselDot);

                if (Number.isInteger(index)) {
                    showSlide(index);
                }
            });
        });


        // Touch and swipe support

        carousel.addEventListener('touchstart', function (event) {

            const target = event.target;

            if (
                target.closest('button') ||
                target.closest('video') ||
                target.closest('input')
            ) {
                isSwiping = false;
                return;
            }

            startX = event.changedTouches[0].clientX;
            startY = event.changedTouches[0].clientY;

            isSwiping = true;

        }, { passive: true });


        carousel.addEventListener('touchend', function (event) {

            if (!isSwiping) {
                return;
            }

            isSwiping = false;

            const endX = event.changedTouches[0].clientX;
            const endY = event.changedTouches[0].clientY;

            const differenceX = startX - endX;
            const differenceY = startY - endY;

            // Ignore vertical scrolling

            if (Math.abs(differenceX) < 50) {
                return;
            }

            if (Math.abs(differenceY) > Math.abs(differenceX)) {
                return;
            }

            if (differenceX > 0) {
                showSlide(currentIndex + 1);
            } else {
                showSlide(currentIndex - 1);
            }

        }, { passive: true });


        // Initialize carousel

        showSlide(0);

    });

});
