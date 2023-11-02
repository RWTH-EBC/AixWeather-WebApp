$("#next_button").click(function() {
    if($("#pills-home-tab").hasClass('active')){
      $("#pills-home-tab").removeClass('active');
      $("#pills-profile-tab").addClass('active');
      $("#pills-home").removeClass('show active');
      $("#pills-profile").addClass('show active');
      document.getElementById("progress").style.width = 50+'%';
      document.getElementById("progress").innerHTML = '50%';
      document.getElementById("back_button").style.visibility = 'visible';

    }
    else if($("#pills-profile-tab").hasClass('active')){
      $("#pills-profile-tab").removeClass('active');
      $("#pills-contact-tab").addClass('active');
      $("#pills-profile").removeClass('show active');
      $("#pills-contact").addClass('show active');
      document.getElementById("progress").style.width = 75+'%';
      document.getElementById("progress").innerHTML = '75%';
      document.getElementById("back_button").style.visibility = 'visible';
    }
    else if($("#pills-contact-tab").hasClass('active')){
      $("#pills-contact-tab").removeClass('active');
      $("#pills-economical-tab").addClass('active');
      $("#pills-contact").removeClass('show active');
      $("#pills-economical").addClass('show active');
      document.getElementById("progress").style.width = 100+'%';
      document.getElementById("progress").innerHTML = '100%';
      document.getElementById("back_button").style.visibility = 'visible';
    }
    else if($("#pills-economical-tab").hasClass('active')){
      $("#pills-economical-tab").removeClass('active');  
      $("#pills-economical").removeClass('show active');     
      document.getElementById("progress").style.width = 100+'%';
      document.getElementById("progress").innerHTML = '100%';
      document.getElementById("back_button").style.visibility = 'visible';
      console.log("Hallo");
      //document.getElementById("result").innerHTML += "<a" + "  href= '{% url &apos; templateapp:progressurl &apos; %}" + ">";      
      document.getElementById("test").href = "result/";
      console.log(document.getElementById("test"));
    }
});

$("#back_button").click(function() {
    if($("#pills-profile-tab").hasClass('active')){
      $("#pills-profile-tab").removeClass('active');
      $("#pills-home-tab").addClass('active');
      $("#pills-profile").removeClass('show active');
      $("#pills-home").addClass('show active');
      document.getElementById("progress").style.width = 25+'%';
      document.getElementById("progress").innerHTML = '25%';
      document.getElementById("back_button").style.visibility = 'hidden';

    }
    else if($("#pills-contact-tab").hasClass('active')){
      $("#pills-contact-tab").removeClass('active');
      $("#pills-profile-tab").addClass('active');
      $("#pills-contact").removeClass('show active');
      $("#pills-profile").addClass('show active');
      document.getElementById("progress").style.width = 50+'%';
      document.getElementById("progress").innerHTML = '50%';
    }
    else if($("#pills-economical-tab").hasClass('active')){
      $("#pills-economical-tab").removeClass('active');
      $("#pills-contact-tab").addClass('active');
      $("#pills-economical").removeClass('show active');
      $("#pills-contact").addClass('show active');
      document.getElementById("progress").style.width = 75+'%';
      document.getElementById("progress").innerHTML = '75%';

    }  

});


$("#pills-home-tab").click(function() {
      document.getElementById("progress").style.width = 25+'%';
      document.getElementById("progress").innerHTML = '25%';
      document.getElementById("back_button").style.visibility = 'hidden';
});

$("#pills-profile-tab").click(function() {
      document.getElementById("progress").style.width = 50+'%';
      document.getElementById("progress").innerHTML = '50%';
      document.getElementById("back_button").style.visibility = 'visible';
});

$("#pills-contact-tab").click(function() {
      document.getElementById("progress").style.width = 75+'%';
      document.getElementById("progress").innerHTML = '75%';
      document.getElementById("back_button").style.visibility = 'visible';
});

$("#pills-economical-tab").click(function() {
      document.getElementById("progress").style.width = 100+'%';
      document.getElementById("progress").innerHTML = '100%';
      document.getElementById("back_button").style.visibility = 'visible';
});

if($("#pills-home-tab").hasClass('active')){
      document.getElementById("back_button").style.visibility = 'hidden';
};

