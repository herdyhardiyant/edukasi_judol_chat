// Chat bottom part offset height adjustment
const inputBoxDiv = document.getElementById("input-box")
const chatOffset = inputBoxDiv.offsetHeight + 40
const emptyOffsetDiv = document.getElementById("chat-empty-offset")
emptyOffsetDiv.style.height = `${chatOffset}px`

// Auto scroll to the bottom of the chat box
emptyOffsetDiv.scrollIntoView({behavior: 'smooth', block: 'start'})

// Image Handling Variables
const selectImageBtn = document.getElementById("select-image-button")
const imgInput = document.getElementById("image-input")
const previewImage =  document.getElementById("image-preview")

const cancelImageUpload =  document.getElementById("cancel-image-upload")

// Image Input
selectImageBtn.addEventListener('click', () => {
    imgInput.click()
})

imgInput.addEventListener('change', (event) => {
    const file = event.target.files[0]
    const reader = new FileReader()

    selectImageBtn.classList.add("d-none")
    previewImage.classList.remove("d-none")
    cancelImageUpload.classList.remove("d-none")

    reader.onload = (event) => {
        previewImage.src = event.target.result
    }

    reader.readAsDataURL(file);
    
})

// Cancel Image Upload / Reset Image
cancelImageUpload.addEventListener("click", (event) => {
    selectImageBtn.classList.remove("d-none")
    previewImage.classList.add("d-none")
    cancelImageUpload.classList.add("d-none")
    previewImage.src = "#"

    imgInput.value = ""
})

// Form Submission
const formSubmission = document.getElementById("form-submission")

formSubmission.addEventListener('submit', async function(params) {
    params.preventDefault()
    const messageContent = document.getElementById("message").value.trim()
    const imageFile = imgInput.files[0]
    
    const formData = new FormData()

    if (messageContent) {
        formData.append("message", messageContent)
    }

    if (imageFile) {
        formData.append("image", imageFile)
    }

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            body: formData
        })

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error)
    }


})