document.addEventListener('DOMContentLoaded', function() {
    const currentMembersContainer = document.getElementById('current_members');
    const addMembersSelector = document.getElementById('add_member_select');
    const addMemberButton = document.getElementById('add_member_button');


    const createTaskContainer = document.getElementById('create_tasks');
    const editContainer = document.getElementById('edit_container');
    const adminButton = document.getElementById('admin_button');
    const adminDiv = document.getElementById('admin_div');

    adminButton.addEventListener('click', () => {
        if (adminDiv.style.display === "none") {adminDiv.style.display = "block";}
        else {adminDiv.style.display = "none";
                resetAllContainers()
}
    })

    document.querySelector("#edit_members").addEventListener('click', () => {
        if (editContainer.style.display === 'none') {
            resetAllContainers()
            editContainer.style.display = "block";
        } else {
            editContainer.style.display = "none";
        }
    })
    currentMembersContainer.addEventListener('click', function (e) {
        if (e.target.id === 'delete_member') {
            const username = e.target.getAttribute('data-username');
            e.target.parentElement.remove();
            removeMember(username);
        }
    })
    addMemberButton.addEventListener('click', () => {
        const selectedOption = addMembersSelector.options[addMembersSelector.selectedIndex];
        const username = selectedOption.textContent;
        const userID = selectedOption.value;
        addMember(username, userID)
    })

    document.querySelector("#create_task").addEventListener('click', () =>{

        if (createTaskContainer.style.display === 'none') {
             resetAllContainers()
            createTaskContainer.style.display = "block";
        } else {
            createTaskContainer.style.display = "none";
        }
    })

    const editTaskContainer = document.getElementById('edit_tasks_container');
    editTaskContainer.addEventListener('click', function(e) {
        if (e.target.id === 'delete_task_button') {
            let taskId = e.target.getAttribute("data-id");
            e.target.parentElement.parentElement.remove();
            deleteTask(taskId);
        }
    })
    function resetAllContainers() {
        editContainer.style.display = 'none';
        createTaskContainer.style.display = 'none';
    }

})
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function removeMember(username){
    let team_name = document.getElementById('team_name').innerText;
    fetch(`/edit_members/${team_name}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // Add CSRF token here
        },
        body: JSON.stringify({
            remove: username
        })
    })
        .then(res => res.json())
        .then(data => {
            const addMembersSelector = document.getElementById('add_member_select');
            const newOption = document.createElement('option');
            newOption.value=username
            newOption.textContent=username
            addMembersSelector.appendChild(newOption)
            if (data.error){
                console.log(data.error)
            }
        })
}

function addMember(username,userID){
    let team_name = document.getElementById('team_name').innerText;
    fetch(`/edit_members/${team_name}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // Add CSRF token here
        },
        body: JSON.stringify({
            "add": username
        })
    })
        .then(res => res.json())
        .then(data => {
            const currentMembersContainer = document.getElementById('current_members');

            const newMemberRow = document.createElement('div');
            newMemberRow.className = "row"
            newMemberRow.style = 'justify-content:space-between;margin:30px'

            const deleteButton = document.createElement('button');
            deleteButton.id = "delete_member";
            deleteButton.className = 'btn btn-outline-danger';
            deleteButton.setAttribute('data-username', username);
            deleteButton.textContent = 'Delete Member';

            const newMember = document.createElement("span")
            newMember.textContent = username


            newMemberRow.appendChild(newMember);
            newMemberRow.appendChild(deleteButton);
            currentMembersContainer.appendChild(newMemberRow);
            currentMembersContainer.appendChild(document.createElement('hr'))

            const addMemberSelector = document.getElementById('add_member_select');
            addMemberSelector.querySelector(`option[value="${userID}"]`).remove();
            if (data.error){
                console.log(data.error)
            }
        })
}
function deleteTask(taskId){
    fetch(`/delete_task/${taskId}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // Add CSRF token here
        },

    })
        .then(res => res.json())
        .then(() => {
            const taskTable = document.querySelector('#task_table');
            document.querySelector(`#task_${taskId}`).remove();
        })
}