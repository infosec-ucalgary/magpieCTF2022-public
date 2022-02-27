<html>
<head>
<title>Crack The Safe</title>
<style>
  
        input {
                position: fixed;
                top: 50%;
                left: 50%;
                margin-top: -50px;
                margin-left: -50px;
        }

        b {
                word-wrap: break-word;
                text-align: center;
        }
        body {
                background-color: #000
        }
        h1 {
                color: #FFD700;
                text-align: center;
        }
        h3 {
                color: #FFD700;
                text-align: center;
        }


</style>
<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
</head>
<body>
<img src="nothingHere.png" width='0' height="0"/>
<!-- Form will only accept a certain string length is x -->
<form id='myform' action='' method='get'>
<?php
$fp = fopen('./flag.zip', "rb");
$binary = fread($fp, filesize('./flag.zip'));
$target = base64_encode($binary);
if (isset($_GET['userinput']) && substr($target, 0, strlen($_GET['userinput'])) == $_GET['userinput']) {
        echo "<input type='text' id='userinput' name='userinput' oninput='doSubmit()' value='".$_GET['userinput']."' autofocus /><br>";
        if ($target == $_GET['userinput']) {
                echo "<b id='useroutput' class='someClass' style='text-align: center; color: #00FF00;'>" . $_GET['userinput'] . "</b>";
        } else {
                echo "<b id='useroutput' class='someClass' style='text-align: center; color: #FF0000;'>" . $_GET['userinput'] . "</b>";
        }
} elseif (strlen($target) < strlen($_GET['userinput'])) { 
        echo "<input type='text' id='userinput' name='userinput' oninput='doSubmit()' value='".$_GET['userinput']."' autofocus /><br>";
        echo "<b id='useroutput' class='someClass' style='text-align: center; color: #00FF00;'>" . $target . "</b>";
} else {
        echo "<input type='text' id='userinput' name='userinput' oninput='doSubmit()' value='' autofocus />";
}
?>
</form>
<script>
function doSubmit() {
        document.getElementById('myform').submit();
}
</script>
<script>
$(document).ready(function() {
        var input = $("#userinput");
        var len = input.val().length;
        input[0].focus();
        input[0].setSelectionRange(len, len);
});
</script>
<h1>Welcome</h1>
<h1>Mom and Pops Very First Flag Shop</h1>
<h3>Enter what you are looking for in text box</h3>
</body>
</html>