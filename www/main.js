$(document).ready(function () {

    

    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });

    //siriwave js configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed:"0.30",
        autostart: true,
      });
    });
    
    //siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "fadeInUp",
            sync: true,
        },
        out:{
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // mic button click event

    $("#Micbtn").click(function () {
        eel.playAssistantSound()
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });


    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    //function to play assistant on getting the typed message
    function playAssistant(message){
        if (message!=""){
            $('#oval').attr('hidden',true);
            $('#SiriWave').attr('hidden',false);
            eel.allCommands(message)()
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    //toggle button to hide and display mic and send button
    function ShowHideButton(message){
        if (message!=""){
            $('#Micbtn').attr('hidden',true);
            $('#Sendbtn').attr('hidden',false);
        }
        else{
            $('#Micbtn').attr('hidden',false);
            $('#Senbtn').attr('hidden',true);
        }
    }

    //keyup event handler on chatbox
    $('#chatbox').keyup(function (){
        let message= $('#chatbox').val();
        ShowHideButton(message)
    });

    //send button click event
    $('#Sendbtn').click(function () {
        let message = $('#chatbox').val()
        playAssistant(message)
    });

