from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import csv
import zipfile
import os

def open_robot_order_website():
    """Opens the website to order robots."""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def close_annoying_modal():
    """Closes the annoying modal that pops up"""
    page = browser.page()
    annoying_modal = page.locator(".btn-dark")
    if annoying_modal.is_visible():
        annoying_modal.click()

def download_csv_file():
    """Downloads csv file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def submit_orders_from_csv_data():
    """Reads the csv orders file and starts to fulfill the orders."""
    with open('orders.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for order in csv_reader:
            fill_the_form(order)
        

def fill_the_form(order):
    """Fills in the order form and submits it."""
    page = browser.page()
    close_annoying_modal()
    page.locator("#head").select_option(order['Head'])
    page.locator(f"#id-body-{order['Body']}").click()
    page.locator("xpath=//label[contains(.,'3. Legs:')]/../input").fill(order['Legs'])
    page.locator("#address").fill(order['Address'])
    page.locator("#order").click()

    error_alert = page.locator(".alert-danger")
    if error_alert:
        while error_alert is not None and error_alert.is_visible():
            print("Error in the order form. Retrying...")
            page.locator("#order").click()
            error_alert = page.locator(".alert-danger")
    
    page.locator("#receipt").wait_for()

    pdf_file_path = store_receipt_as_pdf(order['Order number'])
    image_file_path = screenshot_robot(order['Order number'])
    embed_screenshot_to_receipt(image_file_path, pdf_file_path)

    page.locator("#order-another").click()     


def store_receipt_as_pdf(order_number: int) -> str:
    """Stores the receipt as a PDF file."""
    
    pdf_file_path = f"output/{order_number}.pdf"
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(content=receipt_html, output_path=pdf_file_path)

    return pdf_file_path
    
def screenshot_robot(order_number: int)  -> str:
    """Takes a screenshot of the robot ordered."""
    image_file_path = f"output/{order_number}.png"
    image_locator = browser.page().locator("#robot-preview-image")
    image = browser.screenshot(element=image_locator)
    with open(image_file_path, 'wb') as file:
        file.write(image)
    return image_file_path

def embed_screenshot_to_receipt(screenshot, pdf_file):
    """Embeds the screenshot to the PDF receipt."""
    pdf = PDF()
    pdf.add_files_to_pdf(
        files=[screenshot],
        target_document=pdf_file,
        append=True
    )

def archive_receipts():
    """Archives the receipts to a zip file."""

    # Get all pdf files in the output folder
    files_to_zip = [f"output/{file}" for file in os.listdir("output") if file.endswith(".pdf")]
    with zipfile.ZipFile('output/receipts.zip', 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file)

def delete_old_files():
    files_to_delete = [f"output/{file}" for file in os.listdir("output") if file.endswith(".pdf") or file.endswith(".png") or file.endswith(".zip")]
    for file in files_to_delete:
        os.remove(file)

@task
def order_robots_from_RobotSpareBin():
    browser.configure(
        slowmo=100,
    )
    delete_old_files()
    open_robot_order_website()
    download_csv_file()
    submit_orders_from_csv_data()
    archive_receipts()
