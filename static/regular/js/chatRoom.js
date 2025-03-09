const productId = "{{ chat_room.product.id }}";
const buyerId = "{{ chat_room.buyer.id }}";
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${productId}/${buyerId}/`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><b>${data.author}</b>: ${data.message}</p>`;
};

socket.onclose = function(event) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector("form").onsubmit = function(event) {
    event.preventDefault();
    const input = document.querySelector("input[name='text']");
    socket.send(JSON.stringify({ 'message': input.value }));
    input.value = "";
};