import zlib
from pypdf import PdfReader

def extract_js(pdf_path):
    """
    Extracts JavaScript from a PDF file.
    Scans through all objects for /JS or /JavaScript keys.
    """
    extracted_js = []
    
    try:
        reader = PdfReader(pdf_path)
        
        # pypdf allows accessing all objects in the PDF
        for obj_id in reader.objects:
            obj = reader.objects[obj_id]
            
            # Check if it's a dictionary-like object
            if hasattr(obj, "get"):
                js_content = None
                
                # Look for /JS or /JavaScript keys
                if "/JS" in obj:
                    js_content = obj["/JS"]
                elif "/JavaScript" in obj:
                    js_content = obj["/JavaScript"]
                
                if js_content:
                    # If it's a reference to another object, resolve it
                    if hasattr(js_content, "get_object"):
                        js_content = js_content.get_object()
                    
                    # If it's a stream, we need to read and potentially decompress it
                    if hasattr(js_content, "get_data"):
                        try:
                            extracted_js.append(js_content.get_data().decode('utf-8', errors='ignore'))
                        except Exception:
                            # Sometimes get_data handles decompression, sometimes we might need manual zlib
                            pass
                    elif isinstance(js_content, str):
                        extracted_js.append(js_content)
                    elif isinstance(js_content, bytes):
                        extracted_js.append(js_content.decode('utf-8', errors='ignore'))
                        
    except Exception as e:
        print(f"[!] Error parsing PDF: {e}")
        
    return "\n\n".join(extracted_js)
