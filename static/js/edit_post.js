
const captionInput = document.getElementById('id_caption');
const captionCounter = document.getElementById('caption-counter');
const previewCaption = document.getElementById('preview-caption');

const fileInput = document.getElementById('id_files');
const previewMedia = document.getElementById('preview-media');

if (captionInput) {
    captionInput.addEventListener('input', () => {
        previewCaption.textContent = captionInput.value;
        captionCounter.textContent = captionInput.value.length;
    });
}

if (fileInput) {
    fileInput.addEventListener('change', () => {
        previewMedia.innerHTML = '';

        const files = Array.from(fileInput.files);

        files.forEach(file => {
            const url = URL.createObjectURL(file);

            if (file.type.startsWith('image/')) {
                const image = document.createElement('img');

                image.src = url;
                image.alt = 'New post image';

                previewMedia.appendChild(image);
            }

            else if (file.type.startsWith('video/')) {
                const video = document.createElement('video');

                video.src = url;
                video.controls = true;

                previewMedia.appendChild(video);
            }
        });
    });
}
