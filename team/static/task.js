document.addEventListener('DOMContentLoaded', () => {
    const progressDiv = document.querySelector('#progress_div');
    progressDiv.addEventListener('click', (e) => {
        if(e.target.id === "edit_button") {
            const value = e.target.value;
            if (value === "progress_description") {
                e.target.parentElement.innerHTML=`<h5 style="width:80%"> <strong> New Update: </strong> <input id ="description_input" type="text" placeholder = "Enter Progress Description"> </h5> <button id="save_description" class="btn btn-primary"> Save </button> `
                const saveButton = document.querySelector(`#save_description`);
                saveButton.addEventListener("click", () => {
                    let newContent = document.querySelector(`#description_input`).value;
                    if(newContent){
                        edit_progress(value, newContent)
                    }
                    else{
                        console.log("ERROR:MUST INPUT INFORMATION")
                    }

                })
            }
            else{
                e.target.parentElement.innerHTML=`<h5 style="width:80%"> <strong> New Update: </strong> <input required id ="progress_input" type="number" min="0" max="100" placeholder = "%"> </h5> <button id="save_progress" class="btn btn-primary"> Save </button> `
                const saveButton = document.querySelector(`#save_progress`);
                saveButton.addEventListener("click", () => {
                    let newContent = document.querySelector(`#progress_input`).value;
                    if(newContent){
                        if(newContent >= 0 && newContent <=100) {
                            edit_progress(value, newContent)
                        }
                        else{
                            alert("ERROR:VALUE MUST BE BETWEEN 0 AND 100")
                        }
                    }
                    else{
                        console.log("ERROR:MUST INPUT INFORMATION")
                    }
                })
            }
        }
    })
})

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function edit_progress(featureChanged,newContent){
    const urlPath = window.location.pathname;
    const taskId = urlPath.split('/')[2];  // Assuming the URL is /task/<task_id>
    console.log(taskId);
    fetch(`/report_progress/${taskId}/${featureChanged}`,{
        method: `PUT`,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            body: newContent
        })
    })
        .then(res => res.json())
        .then(() =>{
            window.location.reload()
        })
}
