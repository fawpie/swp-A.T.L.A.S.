import re

def parse_program(file_path="program.txt"):
    """
    program.txt dosyasını okur ve görevleri içeren bir yapıya dönüştürür.
    Satır başındaki girintileri (indentation) korur.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None

    program_data = {"header": "", "weeks": []}
    current_division = None
    
    header_lines = [lines[0].strip()] if lines else []
    if len(lines) > 1: header_lines.append(lines[1].strip())
    program_data["header"] = "\n".join(header_lines)

    for line in lines[2:]:
        # Satır sonundaki boşlukları temizle, baştakileri koru
        line = line.rstrip()
        
        if not line.strip(): # Boş satırları atla
            continue
        
        # Gün, Hafta veya Ay başlıklarını ara
        division_match = re.match(r"--- ((?:GÜN|HAFTA|AY) .*) ---", line.strip(), re.IGNORECASE)
        if division_match:
            current_division = {"title": division_match.group(1), "tasks": []}
            program_data["weeks"].append(current_division)
            continue
            
        # Görev satırlarını ekle
        if line.strip().startswith("[ ]") and current_division is not None:
            current_division["tasks"].append(line)
            
    return program_data