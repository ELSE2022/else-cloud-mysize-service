/**
 * Convert a `File` object returned by the upload input into
 * a base 64 string. That's easier to use on FakeRest, used on
 * the ng-admin example. But that's probably not the most optimized
 * way to do in a production database.
 */
const convertFileToBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file.rawFile);
    reader.onload = () => resolve({ src: reader.result, title: file.name});
    reader.onerror = reject;
});

/**
 * For posts update only, convert uploaded image in base 64 and attach it to
 * the `picture` sent property, with `src` and `title` attributes.
 */
const addUploadCapabilities = requestHandler => (type, resource, params) => {
    if ((type === 'UPDATE' && (resource === 'products' || resource === 'models')) || (type === 'CREATE' && resource === 'models')) {
        if (params.data.files && params.data.files.length) {
            // only freshly dropped pictures are instance of File
            const formerPictures = params.data.files.filter(p => !(p instanceof File));
            // const newPictures = params.data.files.filter(p => p instanceof File);
            return Promise.all(formerPictures.map(convertFileToBase64))
                .then(transformedNewPictures => requestHandler(type, resource, {
                    ...params,
                    data: {
                        ...params.data,
                        files: transformedNewPictures,
                    },
                }));
        }
    }

    return requestHandler(type, resource, params);
};

export default addUploadCapabilities;
