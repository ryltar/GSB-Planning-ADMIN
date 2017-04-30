socket = io.connect('http://localhost:8080',{
          'reconnection': true,
          'reconnectionDelay': 500,
          'reconnectionAttempts': Infinity
})

pseudo = document.cookie.replace(/(?:(?:^|.*;\s*)notice\s*\=\s*([^;]*).*$)|^.*$/, "$1");
pseudo = pseudo.replace('"'," ")
pseudo = pseudo.replace('"'," ")

socket.emit('nouveau_client', pseudo);
socket.emit('subscribe', 'admin')

$( document ).ready(function() {
    socket.on('message', function(data) {
        insereMessage(data.pseudo, data.message, 'you')});
    socket.on('nouveau_client', function(pseudo) {
        let temp = document.createElement("div")
        let tempClear = document.createElement("div")
        tempClear.className += "clear"
        temp.className += "bubble you"
        temp.innerHTML =  '<p><em>' + pseudo + ' a rejoint le Chat !</em></p>'
        document.getElementById('zone_chat').appendChild(temp)
        document.getElementById('zone_chat').appendChild(tempClear)
    })

    socket.on('terminate', function(data){
        let temp = document.createElement("div")
        let tempClear = document.createElement("div")
        tempClear.className += "clear"
        temp.className += "bubble you"
        temp.innerHTML =  '<p><em>' + data.pseudo + ' a quitté le Chat !</em></p>'
        document.getElementById('zone_chat').appendChild(temp)
        document.getElementById('zone_chat').appendChild(tempClear)
    })


   
});


$(window).on('beforeunload' , function () {
    // Remove the cookie
    document.cookie = 'notice' + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    console.log('oui')
});

	var insereMessage = function(pseudo, mess, who) {
        let message = mess
        let link = document.createElement("a");
		let temp = document.createElement("div");
        link.appendChild(temp);
        if(who == "you"){
           link.onclick = function(){
            $('.user').val(pseudo);
            } 
        }
        
        let tempClear = document.createElement("div")
        tempClear.className += "clear"
        link.className += "myLink"
        temp.className += "bubble "+who
        temp.innerHTML =  '<p><span class="strong">'+ pseudo + '</span><span class="padding">' + message + '</span></p>'
        document.getElementById('zone_chat').appendChild(link)
        document.getElementById('zone_chat').appendChild(tempClear)
        if($('.user').val() != ''){
            socket.emit('message', {message:mess, room:($('.user').val())});
        }else{
            socket.emit('message', {message:mess, room:'admin'});
        }
    }

	var myMessage = function(){
		let message = $('#message').val();
        insereMessage(pseudo, message, 'me');
        $('.user').val('');
        $('#message').val('');
        return false; 
	}




  




    