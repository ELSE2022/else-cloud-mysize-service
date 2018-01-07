const addUploadFile = requestHandler => (type, resource, params) => {
    if (type === 'CREATE' && typeof params.data.files !== 'undefined') {
        let data = params.data;

        let form = new FormData();
        form.set("file", data.files[0].rawFile);
        form.set("name", data.files[0].rawFile.name);

        // Setting content-type will produce next problem on work with spring, I don't know how it'll work on other backend solutions:
        // https://stackoverflow.com/questions/36005436/the-request-was-rejected-because-no-multipart-boundary-was-found-in-springboot
        return fetch(`http://localhost:5000/fitting/models`, {
            method: "POST",
            //For this example we'll make basic auth by providing token encoded credentials from local storage
            // headers: new Headers({'Authorization': localStorage.getItem('token')}),
            body: form
        })
        .then((response) => response.json())
        .then((json) => ( { data: { id: json.id }} ))
    }

    return requestHandler(type, resource, params);
};

export default addUploadFile;