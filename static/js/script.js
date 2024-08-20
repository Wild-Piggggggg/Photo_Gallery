document.addEventListener('DOMContentLoaded', () => {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxContent = document.getElementById('lightbox-content');
    const closeBtn = document.querySelector('.lightbox .close');
    // const deleteButtons = document.querySelectorAll('.delete-btn');

    // 触发图片放大效果
    galleryItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // 判断点击是否在删除按钮上
            if (e.target.classList.contains('delete-btn')){
                e.preventDefault();  // 阻止默认事件
                // e.stopPropagation(); // 阻止事件冒泡
                const filename = e.target.getAttribute('data-filename');

                if (confirm('Are you sure you want to delete this photo?')) {
                    fetch('/delete_photo', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ filename: filename })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Photo deleted successfully!');
                            item.remove(); // 从 DOM 中移除图片
                        } else {
                            alert('Failed to delete photo.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Failed to delete photo.');
                    });
                }
                return;
            }
            // 触发图片放大效果
            if (item.id != 'upload-item'){
                const imgSrc = item.querySelector('img').src;
                lightboxContent.src = imgSrc;
                lightbox.style.display = 'flex';
            }
            
        });
    });

    // 修改图片src
    document.querySelectorAll('img.lazy').forEach(img => {
        img.addEventListener('click', function() {
            const thumbnailSrc = img.src;  // 保存缩略图路径
            img.src = img.dataset.full;  // 更改为高质量图片路径

            // 恢复缩略图路径
            closeBtn.addEventListener('click', () => {
                img.src = thumbnailSrc;
                lightbox.style.display = 'none';
            });
        
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) {
                    img.src = thumbnailSrc;
                    lightbox.style.display = 'none';
                }
            });
            lightbox.style.display = 'flex';

        });
    });

    closeBtn.addEventListener('click', () => {
        lightbox.style.display = 'none';
    });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.style.display = 'none';
        }
    });


    // 头像点击触发事件
    const avatar = document.querySelector('.avatar');
    const dropdown = document.querySelector('.dropdown');

    avatar.addEventListener('click', () => {
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', (event) => {
        if (!avatar.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });

    // 上传图片
    const uploadItem = document.getElementById('upload-item');
    const fileInput = document.getElementById('fileInput');

    uploadItem.addEventListener('click', () => {
        fileInput.click(); // 打开文件选择器
    });

    fileInput.addEventListener('change', () => {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Upload successful!');
                location.reload(); // 重新加载页面以刷新画廊
            } else {
                alert('Upload failed.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Upload failed.');
        });
    });
});
