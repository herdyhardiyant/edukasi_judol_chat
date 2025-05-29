
const inputBoxDiv = document.getElementById("input-box")

const chatOffset = inputBoxDiv.offsetHeight + 40

const emptyOffsetDiv = document.getElementById("chat-empty-offset")
emptyOffsetDiv.style.height = `${chatOffset}px`
emptyOffsetDiv.scrollIntoView({behavior: 'smooth', block: 'start'})
