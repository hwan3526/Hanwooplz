let statusOption = document.getElementById('status-select');

if (statusOption) {
    statusOption.addEventListener('change', function () {
        let form = document.getElementById('status-form');
        let formData = new FormData(form);

        formData.append('project_id', projectId);
        fetch('/update-status/', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('모집 상태가 변경되었습니다.');
                } else {
                    alert('변경 실패');
                }
            });
    });

    if (projectStatus === '0') {
        statusOption.selectedIndex = 2;
    } else if (projectStatus === '1') {
        statusOption.selectedIndex = 0;
    } else {
        statusOption.selectedIndex = 1;
    }
}


