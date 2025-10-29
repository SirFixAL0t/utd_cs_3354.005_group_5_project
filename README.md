<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Random Demo Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background-color: #f0f0f0;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Welcome to Our Project!</h1>
    <p>Click the button to see a random number:</p>
    <button onclick="showRandomNumber()">Generate Number</button>
    <p id="result"></p>

    <script>
        function showRandomNumber() {
            const randomNum = Math.floor(Math.random() * 100) + 1;
            document.getElementById("result").innerText = "Random Number: " + randomNum;
        }
    </script>
</body>
</html>
