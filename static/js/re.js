document.addEventListener('DOMContentLoaded', function() {
    if (error!== "") {
        let message;
        switch (error) {
            case 'username_exists':
                message = 'Username already exists, please choose another one.';
                break;
            case 'database_error':
                message = 'An error occurred while registering. Please try again.';
                break;
            case 'Username does not exist.':
                message = 'Username does not exist. Please try again.';
                break;
            case 'Incorrect password.':
                message = 'Incorrect password. Please try again.';
                break;
            default:
                message = 'An unknown error occurred.';
        }
        // 在模态框的主体部分插入错误信息
        document.querySelector('#errorModal .modal-body').textContent = message;
        // 使用 Bootstrap 的 JavaScript 方法显示模态框
        $('#errorModal').modal('show');
    }
});