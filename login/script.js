const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
	container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
	container.classList.add("right-panel-active");
});

fistForm.addEventListener("submit", function(e) {
		var params = {  "name" : e.target[0].value,
	 			   		"surname" : e.target[1].value,
		  		 		"address" : e.target[2].value,
		 				"email" : e.target[3].value,
		 				"password" : e.target[4].value
		};
		fetch("http://metuchatbot.com:8000/signup", { 
			method: "POST",
			headers: {
		    Accept: "application/json",
		    	"Content-Type": "application/json"
		  	},
    		body: JSON.stringify(params)
    	}).then((Response) => {
        	return Response.json()
    	}).then((data) => {
      		if (data.message == "Signup Completed") {
    			setCookie(params.email);
    			window.location.replace("http://metuchatbot.com/chatbot");
    		}
    		else {
    				window.alert(data.message);
    			}
        })
}
	);
secondForm.addEventListener("submit", function(e) {

		var params = {  "email" : e.target[0].value,
		 				"password" : e.target[1].value
		};
		fetch("http://metuchatbot.com:8000/login", { 
			method: "POST",
			headers: {
		    Accept: "application/json",
		    	"Content-Type": "application/json"
		  	},
    		body: JSON.stringify(params)
    	}).then((Response) => {
        	return Response.json()
    	}).then((data) => {
    		setTimeout(function() {
			    if (data.message == "Its Valid") {
    			setCookie(params.email);
    			window.location.replace("http://metuchatbot.com/chatbot");
    			}
    			else {
    				window.alert(data.message);
    			}
			  }, 1000);
    		
      		
        })
}
);
function setCookie(email){
	const d = new Date();
	d.setTime(d.getTime() + (30 * 24 * 60 * 60 * 1000));
	let expires = "expires="+d.toUTCString();
	document.cookie = email + ";" + expires + ";path=/";
}