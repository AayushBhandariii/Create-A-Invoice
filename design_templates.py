# Swiss style template
TEMPLATE_BRUTALIST = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @page { size: A4; margin: 0; }
        body { -webkit-print-color-adjust: exact; font-family: 'Helvetica Neue', Arial, sans-serif; }
    </style>
</head>
<body class="bg-[#1c1c1e] p-8 flex justify-center items-start min-h-screen">
    <div class="w-full max-w-[800px] bg-white text-black p-12 shadow-2xl flex flex-col justify-between min-h-[1050px]">
        <div>
            <div class="flex justify-between items-baseline border-b-[3px] border-black pb-4">
                <h2 class="text-4xl font-black tracking-tighter uppercase">{{ from_name.split(' ')[0] }}.</h2>
                <span class="text-sm font-bold tracking-widest uppercase font-mono">SECURE RECORD // INVOICE</span>
            </div>
            <div class="grid grid-cols-2 gap-8 mt-10 text-xs">
                <div>
                    <p class="font-bold uppercase tracking-wider text-[#71717a] mb-2 text-[10px]">ISSUED BY</p>
                    <p class="font-bold text-sm tracking-tight">{{ from_name }}</p>
                    <p class="whitespace-pre-line text-[#27272a] leading-relaxed mt-1 font-mono text-[11px]">{{ from_details }}</p>
                </div>
                <div>
                    <p class="font-bold uppercase tracking-wider text-[#71717a] mb-2 text-[10px]">PREPARED FOR</p>
                    <p class="font-bold text-sm tracking-tight">{{ to_name }}</p>
                    <p class="whitespace-pre-line text-[#27272a] leading-relaxed mt-1 font-mono text-[11px]">{{ to_details }}</p>
                </div>
            </div>
            <div class="grid grid-cols-4 gap-4 border-t border-b border-black py-4 mt-12 text-xs font-mono">
                <div><p class="text-[9px] uppercase font-bold text-[#71717a] mb-1 font-sans">REF ID</p><p class="font-bold">{{ invoice_number }}</p></div>
                <div><p class="text-[9px] uppercase font-bold text-[#71717a] mb-1 font-sans">DATE</p><p>{{ issue_date }}</p></div>
                <div><p class="text-[9px] uppercase font-bold text-[#71717a] mb-1 font-sans">DUE CLOSE</p><p class="font-bold">{{ due_date }}</p></div>
                <div class="text-right"><p class="text-[9px] uppercase font-bold text-[#71717a] mb-1 font-sans">CURRENCY</p><p class="font-bold">{{ currency_iso }}</p></div>
            </div>
            <div class="mt-10">
                <table class="w-full text-left text-xs font-mono">
                    <thead>
                        <tr class="border-b-2 border-black font-sans text-[10px] uppercase font-bold tracking-wider text-[#71717a]">
                            <th class="pb-2">Line Particulars</th>
                            <th class="pb-2 text-right w-20">Qty</th>
                            <th class="pb-2 text-right w-28">Unit Cost</th>
                            <th class="pb-2 text-right w-28">Net Value</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        {% for item in items %}
                        <tr>
                            <td class="py-3 font-sans font-bold text-sm tracking-tight">
                                {{ item.title }}
                                {% if item.description %}<p class="text-xs text-[#52525b] font-sans font-normal max-w-[420px] leading-relaxed mt-1">{{ item.description }}</p>{% endif %}
                            </td>
                            <td class="py-3 text-right">{{ "%.2f"|format(item.quantity) }}</td>
                            <td class="py-3 text-right">{{ item.formatted_unit_price }}</td>
                            <td class="py-3 text-right font-bold">{{ item.formatted_total_price }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="mt-8 flex justify-end">
                <div class="w-64 font-mono text-xs space-y-2 border-t-2 border-black pt-4">
                    <div class="flex justify-between"><span class="text-[#52525b]">Gross Subtotal</span><span>{{ formatted_subtotal }}</span></div>
                    <div class="flex justify-between"><span class="text-[#52525b]">Service Tax ({{ tax_rate_percent }}%)</span><span>{{ formatted_tax }}</span></div>
                    <div class="flex justify-between text-sm font-bold border-t border-gray-200 pt-2 font-sans"><span>TOTAL SUM</span><span>{{ formatted_total }}</span></div>
                </div>
            </div>
        </div>
        <div class="border-t border-black pt-6 flex justify-between items-end text-[9px] text-[#52525b] font-mono mt-16">
            <div>
                <p class="font-sans font-bold uppercase text-black text-[10px]">Settlement Policy</p>
                <p>Assets initialized upon full settlement verification. Late cycles trigger a cumulative 10% interest run.</p>
            </div>
            <div class="text-right"><p class="font-sans font-bold text-black text-xs uppercase tracking-widest">{{ from_name }}</p></div>
        </div>
    </div>
</body>
</html>
"""

# Corporate Minimalist Template

TEMPLATE_MINIMALIST = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @page { size: A4; margin: 0; }
        body { -webkit-print-color-adjust: exact; font-family: 'Inter', system-ui, sans-serif; }
    </style>
</head>
<body class="bg-gray-100 p-8 flex justify-center items-start min-h-screen">
    <div class="w-full max-w-[800px] bg-white text-gray-900 p-16 shadow-xl flex flex-col justify-between min-h-[1050px]">
        <div>
            <div class="flex justify-between items-start">
                <div>
                    <h1 class="text-2xl font-light tracking-tight text-gray-500 uppercase">Statement</h1>
                    <p class="text-xs text-gray-400 mt-0.5 font-mono"># {{ invoice_number }}</p>
                </div>
                <div class="text-right">
                    <p class="font-bold text-base tracking-tight text-black">{{ from_name }}</p>
                    <p class="whitespace-pre-line text-xs text-gray-500 mt-1 font-mono leading-tight">{{ from_details }}</p>
                </div>
            </div>
            
            <div class="mt-16 border-t border-gray-100 pt-8 grid grid-cols-3 gap-4 text-xs">
                <div>
                    <span class="text-gray-400 font-medium block mb-1">Client Contact</span>
                    <p class="font-semibold text-gray-900">{{ to_name }}</p>
                    <p class="whitespace-pre-line text-gray-500 font-mono mt-1 leading-tight">{{ to_details }}</p>
                </div>
                <div>
                    <span class="text-gray-400 font-medium block mb-1">Timeline Placement</span>
                    <p class="text-gray-600 font-mono">Issued: {{ issue_date }}</p>
                    <p class="text-gray-900 font-semibold font-mono mt-0.5">Due: {{ due_date }}</p>
                </div>
                <div class="text-right">
                    <span class="text-gray-400 font-medium block mb-1">Amount Due</span>
                    <p class="text-2xl font-bold tracking-tight text-black font-mono">{{ formatted_total }}</p>
                </div>
            </div>

            <table class="w-full mt-16 text-left text-xs">
                <thead>
                    <tr class="text-gray-400 border-b border-gray-100 pb-2 text-[11px] font-medium">
                        <th class="pb-3 font-normal">Description Specifications</th>
                        <th class="pb-3 text-right font-normal w-16">Qty</th>
                        <th class="pb-3 text-right font-normal w-24">Rate</th>
                        <th class="pb-3 text-right font-normal w-24">Amount</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    {% for item in items %}
                    <tr class="text-gray-700">
                        <td class="py-4 font-medium text-gray-900">
                            {{ item.title }}
                            {% if item.description %}<p class="text-gray-400 font-normal text-xs mt-0.5 max-w-md leading-relaxed">{{ item.description }}</p>{% endif %}
                        </td>
                        <td class="py-4 text-right font-mono text-gray-500">{{ "%.1f"|format(item.quantity) }}</td>
                        <td class="py-4 text-right font-mono text-gray-500">{{ item.formatted_unit_price }}</td>
                        <td class="py-4 text-right font-mono font-semibold text-gray-900">{{ item.formatted_total_price }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <div class="mt-8 flex justify-end">
                <div class="w-60 text-xs space-y-2 pt-4">
                    <div class="flex justify-between text-gray-400"><span>Subtotal</span><span class="font-mono text-gray-600">{{ formatted_subtotal }}</span></div>
                    <div class="flex justify-between text-gray-400"><span>Vat/Tax ({{ tax_rate_percent }}%)</span><span class="font-mono text-gray-600">{{ formatted_tax }}</span></div>
                    <div class="flex justify-between text-sm font-semibold border-t border-gray-100 pt-3 text-black"><span>Total Balance</span><span class="font-mono">{{ formatted_total }}</span></div>
                </div>
            </div>
        </div>
        
        <div class="text-[10px] text-gray-400 mt-20 flex justify-between items-center font-mono border-t border-gray-50 pt-4">
            <p>Generated dynamically via Create-A-Invoice </p>
            <p>© 2026</p>
        </div>
    </div>
</body>
</html>
"""

