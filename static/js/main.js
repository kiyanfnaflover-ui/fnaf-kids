document.addEventListener('DOMContentLoaded', () => {
    // 1. Loading Animation Timeout Control
    const loader = document.getElementById('loader');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.style.transition = 'opacity 0.5s ease';
                loader.style.opacity = '0';
                setTimeout(() => loader.style.display = 'none', 500);
            }, 2500); // System holds load display for 2.5 seconds
        });
    }

    // 2. Dynamic Media & Storage Parser Engine
    if (document.getElementById('comic-list')) {
        fetch('/api/data')
            .then(res => res.json())
            .then(data => {
                // Populate PDF Comic Reader Layout
                const comicList = document.getElementById('comic-list');
                if(data.comics.length === 0) comicList.innerHTML = '<p class="empty">No comics uploaded to mainframes yet.</p>';
                data.comics.forEach(pdf => {
                    comicList.innerHTML += `
                        <div class="comic-frame">
                            <h4>📖 ${pdf.replace('.pdf', '')}</h4>
                            <iframe src="/uploads/comics/${pdf}#toolbar=0"></iframe>
                        </div>
                    `;
                });

                // Populate Media Elements (Images and Video Edits)
                const galleryGrid = document.getElementById('gallery-grid');
                if(data.gallery.length === 0) galleryGrid.innerHTML = '<p class="empty">Security logs are completely empty.</p>';
                data.gallery.forEach(media => {
                    const isVideo = media.endsWith('.mp4');
                    galleryGrid.innerHTML += `
                        <div class="media-card">
                            ${isVideo ? `<video src="/uploads/gallery/${media}" controls></video>` : `<img src="/uploads/gallery/${media}" />`}
                            <p style="text-align:center; margin-top:5px;">${media}</p>
                        </div>
                    `;
                });

                // Populate Extracted Txt Links System
                const linksList = document.getElementById('links-list');
                if(data.links.length === 0) linksList.innerHTML = '<li>No transmissions found.</li>';
                data.links.forEach(link => {
                    linksList.innerHTML += `
                        <li>📡 Broadcast Link Found: <a href="${link}" target="_blank">${link}</a></li>
                    `;
                });
            });
    }
});