function toggleCodeInput() {
    const isChecked = document.getElementById('test_mod').checked;
    const updateCodeInput = document.getElementById('update_code').parentNode;
    const dumpCodeInput = document.getElementById('dump_code').parentNode;
    
    if (isChecked) {
        updateCodeInput.classList.add('hidden');
        dumpCodeInput.classList.add('hidden');
    } else {
        updateCodeInput.classList.remove('hidden');
        dumpCodeInput.classList.remove('hidden');
    }
}

function handleUpdate() {
    const formData = new FormData();
    formData.append('username', document.getElementById('update_username').value);
    formData.append('email', document.getElementById('update_email').value);
    formData.append('code', document.getElementById('update_code').value);
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/update', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && (xhr.status === 403)){
            alert(JSON.parse(xhr.responseText)['error']);
        }

        else if (xhr.readyState === 4 && xhr.status === 400){
            alert(JSON.parse(xhr.responseText)['error']);
            location.href = '/';
        }

        else if (xhr.readyState === 4 && xhr.status === 200) {
            alert(JSON.parse(xhr.responseText)['message']);
            location.href = '/';
        }
    };
    xhr.send(formData);
}

function handleDump() {
    const formData = new FormData();
    formData.append('username', document.getElementById('dump_username').value);
    formData.append('path', document.getElementById('dump_path').value);
    formData.append('code', document.getElementById('dump_code').value);
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/dump', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && (xhr.status === 403 || xhr.status === 400)){
            alert(JSON.parse(xhr.responseText)['error']);
        }

        else if (xhr.readyState === 4 && xhr.status === 400){
            alert(JSON.parse(xhr.responseText)['error']);
            location.href = '/';
        }

        else if (xhr.readyState === 4 && xhr.status === 200) {
            alert('Dump Results: ' + xhr.responseText);
            location.href = '/';
        }
    };
    xhr.send(formData);
}