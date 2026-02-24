
const wrapper = document.querySelector(".wrapper");
const fileName = document.querySelector(".file-name");
const defaultBtn = document.querySelector("#default-btn");
const customBtn = document.querySelector("#custom-btn");
const cancelBtn = document.querySelector("#cancel-btn i");
const img = document.querySelector("#foodimage");
const imgform=document.querySelector("#foodimgform");
let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

function defaultBtnActive(){
    defaultBtn.click();    
}
defaultBtn.addEventListener("change", function(){
    const file = this.files[0];
    if(file){
    const reader = new FileReader();
    reader.onload = function(){
        const result = reader.result;
        img.src = result;
        console.log(result)
        wrapper.classList.add("active");
        document.getElementById("info").style.display = "none";
        document.getElementById("loading").style.display = "block";
        imgform.submit();
        
    }
    cancelBtn.addEventListener("click", function(){
        img.src = "";
        wrapper.classList.remove("active");
        window.location.href = "";
        
    })
    
    reader.readAsDataURL(file);
    }
    if(this.value){
    let valueStore = this.value.match(regExp);
    fileName.textContent = valueStore;
    
    }
});

function myFunctab1() {
    document.getElementById("tab2").style.display = "none";
    document.getElementById("tab1").style.display = "block";
    document.getElementById("tabbtn2").className="nav-link"
    document.getElementById("tabbtn1").className="nav-link active"
    
    
}

function myFunctab2() {
    document.getElementById("tab1").style.display = "none";
    document.getElementById("tab2").style.display = "block";
    document.getElementById("tabbtn1").className="nav-link"
    document.getElementById("tabbtn2").className="nav-link active"
}

function select(filename){
    img.src = "/static/images/"+filename
    wrapper.classList.add("active");
    document.getElementById("info").style.display = "none";
    document.getElementById("loading").style.display = "block";
    document.getElementById("close").click()
}


    
    

// Dark Mode Toggle Logic
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

// Check for saved theme preference in localStorage
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeIcon.classList.replace('fa-moon', 'fa-sun');
}

if(themeToggleBtn){
    themeToggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        
        // Update the icon and save preference
        if (document.body.classList.contains('dark-mode')) {
            themeIcon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
}
