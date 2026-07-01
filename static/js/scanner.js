async function onScanSuccess(decodedText, decodedResult) {
    scanner.clear()
    const response = await fetch(`/lookup/${decodedText}`);
    const data = await response.json();
    console.log(data);

    document.getElementById("name").value = data.name;
    document.getElementById("category").value = data.category;
    document.getElementById("barcode").value = decodedText;

    document.getElementById("product-form").style.display = "block";
}

async function handleAddProduct(){

    const originalPrice = document.getElementById("original_price").value;
    const expiry = document.getElementById("expiry").value;
    const stock = document.getElementById("stock").value;
    const barcode = document.getElementById("barcode").value;
    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;

    console.log("name:", name, "category:", category, "barcode:", barcode, "Stock:", stock, "Expiry:", expiry, "Original Price:", originalPrice)

    const product = {name, category, barcode, stock, expiry, original_price: originalPrice}

    const response = await fetch("/save", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(product)
    });

    const result = await response.json();
    console.log(result);

}

document.getElementById("submit_button").addEventListener("click", handleAddProduct)


function onScanFailure(error) {
    console.warn(`Code scan error = ${error}`);
}

let scanner = new Html5QrcodeScanner("reader", {fps: 10, qrbox: 250});
scanner.render(onScanSuccess, onScanFailure);