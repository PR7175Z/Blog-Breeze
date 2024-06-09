featuredimage.onchange = evt => {
    const [file] = featuredimage.files
    if (file) {
        fimg.src = URL.createObjectURL(file)
    }
}