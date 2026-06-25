import sys
import asyncio
from datetime import datetime, timedelta
from jinja2 import Template
from playwright.async_api import async_playwright
from babel.numbers import format_currency
from design_templates import TEMPLATE_BRUTALIST, TEMPLATE_MINIMALIST

TEMPLATE_MAP = {
    "1": TEMPLATE_BRUTALIST,
    "2": TEMPLATE_MINIMALIST
}

# Core processing pipeline
def process_global_invoice(data, currency, locale):
    tax_rate = data['tax_rate_percent']
    subtotal_cents = 0
    processed_items = []

    babel_currency = "NPR" if currency == "NRS" else currency

    for item in data['items']:
        qty = item['quantity']
        price_cents = int(round(item['unit_price'] * 100))
        total_item_cents = int(round(qty * price_cents))
        subtotal_cents += total_item_cents

        raw_unit = format_currency(price_cents / 100, babel_currency, format='¤¤ #,##0.00', locale=locale)
        raw_total = format_currency(total_item_cents / 100, babel_currency, format='¤¤ #,##0.00', locale=locale)

        processed_items.append({
            **item,
            "formatted_unit_price": raw_unit.replace("NPR", "NRS"),
            "formatted_total_price": raw_total.replace("NPR", "NRS")
        })

    tax_cents = int(round(subtotal_cents * (tax_rate / 100)))
    total_cents = subtotal_cents + tax_cents

    subtotal_str = format_currency(subtotal_cents / 100, babel_currency, format='¤¤ #,##0.00', locale=locale)
    tax_str = format_currency(tax_cents / 100, babel_currency, format='¤¤ #,##0.00', locale=locale)
    total_str = format_currency(total_cents / 100, babel_currency, format='¤¤ #,##0.00', locale=locale)

    return {
        **data,
        "currency_iso": currency,
        "items": processed_items,
        "formatted_subtotal": subtotal_str.replace("NPR", "NRS"),
        "formatted_tax": tax_str.replace("NPR", "NRS"),
        "formatted_total": total_str.replace("NPR", "NRS")
    }

async def generate_invoice(payload, currency, locale, output_path, template_choice):
    render_context = process_global_invoice(payload, currency, locale)
    
    # Pick template layout based on selection index
    raw_html_layout = TEMPLATE_MAP.get(template_choice, TEMPLATE_BRUTALIST)
    
    template = Template(raw_html_layout)
    rendered_html = template.render(render_context)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(rendered_html)
        
        # Guard rails for execution rendering verification
        await page.evaluate("document.fonts.ready")
        
        await page.pdf(
            path=output_path, 
            format="A4", 
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        await browser.close()
    print(f"\n Generation complete. Saved to: {output_path}")

# Terminal CLI input interface
def get_terminal_inputs():
    print("\n" + "="*50)
    print("     CREATE-A-INVOICE        ")
    print("="*50)
    
    print("\n[SELECT DESIGN THEME]")
    print("1) Swiss Brutalist (Bold, Hard Contrast, Mono labels)")
    print("2) Corporate Minimalist (Lean, Light Gray Layout, Elite UI)")
    template_choice = input("Select layout option (1-2, default 1): ").strip() or "1"
    
    invoice_number = input("\nInvoice ID (e.g., INV-001): ").strip() or "INV-001"
    issue_date = input("Issue Date (YYYY-MM-DD, Enter for today): ").strip() or datetime.now().strftime("%Y-%m-%d")
    due_date = input("Due Date (YYYY-MM-DD), Enter for 7 days from today : ").strip() or (datetime.now()+timedelta(days=7)).strftime("%Y-%m-%d") 
    
    print("\n[PARTIES INFORMATION]")

    # 1. Require Business Name
    while True:
        from_name = input("Your Business Name (Required): ").strip()
        if from_name:
            break
        print(" Error: Your Business Name cannot be empty.")
        
    # 2. Require Business Details
    while True:
        from_details = input("Your Contact/Address Details (Required): ").strip()
        if from_details:
            break
        print(" Error: Your Contact/Address Details are required for legal compliance.")
        
    # 3. Require Client Name
    while True:
        to_name = input("Client Name (Required): ").strip()
        if to_name:
            break
        print(" Error: Client Name cannot be empty.")
        
    # 4. Require Client Details
    while True:
        to_details = input("Client Contact/Address Details (Required): ").strip()
        if to_details:
            break
        print(" Error: Client Contact/Address Details are required to process this asset.")
    
    print("\n[CURRENCY MATCH ENGINE]")
    currency_iso = input("Enter Currency Code (e.g., NRS, USD, EUR): ").strip().upper() or "NRS"
    
    if currency_iso == "NRS":
        locale = "en_IN"  
    elif currency_iso == "EUR":
        locale = "de_DE"
    else:
        locale = "en_US"
        
    tax_rate_percent = float(input("Tax/VAT Rate Percentage (e.g., 13): ") or "0")
    
    print("\n[LINE ITEMS]")
    items = []
    while True:
        title = input("\nItem/Service Title: ").strip()
        if not title:
            break
            
        description = input("Sub-description / context (Optional): ").strip()
        quantity = float(input("Quantity: ") or "1.0")
        unit_price = float(input(f"Unit Price/Rate in {currency_iso}: "))
        
        items.append({
            "title": title.upper(),
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price
        })
        
        more = input("Add another line item? (y/N): ").strip().lower()
        if more != 'y':
            break

    output_filename = input("\nOutput filename (e.g., billing.pdf): ").strip() or "billing.pdf"
    
    return {
        "payload": {
            "invoice_number": invoice_number,
            "issue_date": issue_date,
            "due_date": due_date,
            "from_name": from_name,
            "from_details": from_details,
            "to_name": to_name,
            "to_details": to_details,
            "tax_rate_percent": tax_rate_percent,
            "items": items
        },
        "currency": currency_iso,
        "locale": locale,
        "output_filename": output_filename,
        "template_choice": template_choice
    }

if __name__ == "__main__":
    config = get_terminal_inputs()
    asyncio.run(generate_invoice(
        config['payload'], 
        config['currency'], 
        config['locale'], 
        config['output_filename'],
        config['template_choice']
    ))