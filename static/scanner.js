async function onScanSuccess(decodedText, decodedResult) {
    scanner.clear()
    const responce = await fetch(`/lookup/${decodedText}`);
    const data = await responce.json();
    console.log(data);

    document.getElementById("name").value = data.name;
    document.getElementById("category").value = data.category;
    document.getElementById("barcode").value = decodedText;

    document.getElementById("product-form").style.display = "block";
}



function onScanFailure(error) {
    console.warn(`Code scan error = ${error}`);
}

let scanner = new Html5QrcodeScanner("reader", {fps: 10, qrbox: 250});
scanner.render(onScanSuccess, onScanFailure);