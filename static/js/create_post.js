
document.addEventListener('DOMContentLoaded', function () {
    const captionInput = document.getElementById('id_caption');
    const captionPreview = document.getElementById('preview-caption');
    const captionCounter = document.getElementById('caption-counter');

    const fileInput = document.getElementById('id_files');
    const mediaPreview = document.getElementById('preview-media');

    let previewUrls = [];

    // CAPTION PREVIEW

    function updateCaption() {
        const text = captionInput.value.trim();

        captionPreview.textContent = text || 'Your caption will appear here...';
        captionCounter.textContent = captionInput.value.length;
    }

    captionInput.addEventListener('input', updateCaption);

    // MEDIA PREVIEW

    function clearPreviewUrls() {
        previewUrls.forEach(function (url) {
            URL.revokeObjectURL(url);
        });

        previewUrls = [];
    }

    function updateMediaPreview() {
        clearPreviewUrls();

        const files = Array.from(fileInput.files);

        mediaPreview.innerHTML = '';

        if (files.length === 0) {
            mediaPreview.innerHTML = `
                <div class="preview-empty">
                    <span>+</span>
                    <p>Your media will appear here</p>
                </div>
            `;

            return;
        }

        const grid = document.createElement('div');
        grid.className = 'preview-media-grid';

        files.forEach(function (file) {
            const url = URL.createObjectURL(file);
            previewUrls.push(url);

            const item = document.createElement('div');
            item.className = 'preview-media-item';

            if (file.type.startsWith('image/')) {
                const image = document.createElement('img');
                image.src = url;
                image.alt = 'Post preview';

                item.appendChild(image);
            } else if (file.type.startsWith('video/')) {
                const video = document.createElement('video');
                video.src = url;
                video.controls = true;
                video.preload = 'metadata';

                item.appendChild(video);
            } else {
                return;
            }

            grid.appendChild(item);
        });

        mediaPreview.appendChild(grid);
    }

    fileInput.addEventListener('change', updateMediaPreview);

    // INITIAL STATE

    updateCaption();
    updateMediaPreview();
});
