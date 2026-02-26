import ast
import os


def list_keywords_with_decorators(file_path):
    try:
        with open(file_path, 'r') as file:
            node = ast.parse(file.read(), filename=file_path)
            found_keywords = []

            for n in ast.walk(node):
                if isinstance(n, ast.FunctionDef):
                    for decorator in n.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                            found_keywords.append({
                                'function_name': n.name,
                                'decorator': 'keyword',
                                'line': n.lineno
                            })
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                keyword_value = None
                                if decorator.args:
                                    if isinstance(decorator.args[0], ast.Constant):
                                        keyword_value = decorator.args[0].value
                                    elif isinstance(decorator.args[0], ast.Str):
                                        keyword_value = decorator.args[0].s

                                found_keywords.append({
                                    'function_name': n.name,
                                    'decorator': 'keyword',
                                    'keyword_value': keyword_value,
                                    'line': n.lineno
                                })

            return found_keywords

    except FileNotFoundError:
        error_msg = f"{file_path} bulunamadı."
        print(error_msg)
        return []
    except Exception as e:
        error_msg = f"Bir hata oluştu: {e}"
        print(error_msg)
        return []


def list_detailed_keywords(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            node = ast.parse(content, filename=file_path)

            keywords = []
            classes = []

            for n in node.body:
                if isinstance(n, ast.ClassDef):
                    class_info = {
                        'name': n.name,
                        'line': n.lineno,
                        'methods': []
                    }

                    for item in n.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'line': item.lineno,
                                'decorators': []
                            }

                            for decorator in item.decorator_list:
                                if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                                    method_info['decorators'].append({
                                        'type': 'keyword',
                                        'value': None
                                    })
                                elif isinstance(decorator, ast.Call):
                                    if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                        keyword_value = None
                                        if decorator.args:
                                            if hasattr(decorator.args[0], 'value'):
                                                keyword_value = decorator.args[0].value
                                            elif hasattr(decorator.args[0], 's'):
                                                keyword_value = decorator.args[0].s

                                        method_info['decorators'].append({
                                            'type': 'keyword',
                                            'value': keyword_value
                                        })

                            if method_info['decorators']:
                                class_info['methods'].append(method_info)

                    if class_info['methods']:
                        classes.append(class_info)

                elif isinstance(n, ast.FunctionDef):
                    func_info = {
                        'name': n.name,
                        'line': n.lineno,
                        'decorators': []
                    }

                    for decorator in n.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                            func_info['decorators'].append({
                                'type': 'keyword',
                                'value': None
                            })
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                keyword_value = None
                                if decorator.args:
                                    if hasattr(decorator.args[0], 'value'):
                                        keyword_value = decorator.args[0].value
                                    elif hasattr(decorator.args[0], 's'):
                                        keyword_value = decorator.args[0].s

                                func_info['decorators'].append({
                                    'type': 'keyword',
                                    'value': keyword_value
                                })

                    if func_info['decorators']:
                        keywords.append(func_info)

            return {'functions': keywords, 'classes': classes}

    except FileNotFoundError:
        error_msg = f"{file_path} bulunamadı."
        print(error_msg)
        return {'functions': [], 'classes': []}
    except Exception as e:
        error_msg = f"Bir hata oluştu: {e}"
        print(error_msg)
        return {'functions': [], 'classes': []}


def write_results_to_file(file_path, output_file):
    """Keywordleri dosyaya yazar"""

    # Detaylı sonuçları al
    detailed_result = list_detailed_keywords(file_path)

    try:
        # Çıktı dosyasının dizinini kontrol et ve oluştur
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"KEYWORD LISTESI - {file_path}\n")
            f.write(f"Oluşturulma Tarihi: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # Sınıflardaki keyword metodları
            if detailed_result['classes']:
                f.write("SINIFLARDAKI KEYWORD METODLARI:\n")
                f.write("-" * 40 + "\n")
                for class_info in detailed_result['classes']:
                    f.write(f"\nSınıf: {class_info['name']} (satır {class_info['line']})\n")
                    for method in class_info['methods']:
                        for dec in method['decorators']:
                            if dec['value']:
                                f.write(f"  → {method['name']} -> @keyword({dec['value']}) [satır {method['line']}]\n")
                            else:
                                f.write(f"  → {method['name']} -> @keyword [satır {method['line']}]\n")
                f.write("\n")

            # Doğrudan fonksiyonlardaki keywordler
            if detailed_result['functions']:
                f.write("DOĞRUDAN FONKSIYONLARDAKI KEYWORDLER:\n")
                f.write("-" * 40 + "\n")
                for func in detailed_result['functions']:
                    for dec in func['decorators']:
                        if dec['value']:
                            f.write(f"  → {func['name']} -> @keyword({dec['value']}) [satır {func['line']}]\n")
                        else:
                            f.write(f"  → {func['name']} -> @keyword [satır {func['line']}]\n")
                f.write("\n")

            # Özet istatistikler
            f.write("=" * 60 + "\n")
            f.write("ÖZET İSTATİSTİKLER:\n")
            f.write("-" * 40 + "\n")

            total_functions = len(detailed_result['functions'])
            total_classes = len(detailed_result['classes'])
            total_methods = sum(len(class_info['methods']) for class_info in detailed_result['classes'])

            f.write(f"Toplam Keyword Fonksiyon: {total_functions}\n")
            f.write(f"Keyword İçeren Sınıf Sayısı: {total_classes}\n")
            f.write(f"Sınıflardaki Toplam Keyword Metod: {total_methods}\n")
            f.write(f"Toplam Keyword Sayısı: {total_functions + total_methods}\n")
            f.write("=" * 60 + "\n")

        print(f"✓ Sonuçlar başarıyla '{output_file}' dosyasına yazıldı.")
        return True

    except Exception as e:
        print(f"✗ Dosyaya yazma hatası: {e}")
        return False


# Ana kullanım
source_file = 'C:\\Users\\user\\PycharmProjects\\QA_Lab_python\\keylist.py'
output_file = 'C:\\Users\\user\\PycharmProjects\\QA_Lab_python\\keylist.txt'

# Alternatif olarak PracticeSoftWarePage.py için de kullanabilirsiniz:
# source_file = 'C:\\Users\\user\\PycharmProjects\\QA_Lab_python\\pages\\PracticeSoftWarePage.py'

# Sonuçları dosyaya yaz
write_results_to_file(source_file, output_file)

# Ayrıca ekranda da göster (isteğe bağlı)
print("\n" + "=" * 30)
print("EK RANDA GÖRÜNTÜLEME:")
print("=" * 30)

detailed_result = list_detailed_keywords(source_file)

print("\nSınıflardaki keyword metodları:")
for class_info in detailed_result['classes']:
    print(f"\nSınıf: {class_info['name']}")
    for method in class_info['methods']:
        for dec in method['decorators']:
            if dec['value']:
                print(f"  - {method['name']} -> @keyword({dec['value']})")
            else:
                print(f"  - {method['name']} -> @keyword")

print("\nDoğrudan fonksiyonlardaki keywordler:")
for func in detailed_result['functions']:
    for dec in func['decorators']:
        if dec['value']:
            print(f"- {func['name']} -> @keyword({dec['value']})")
        else:
            print(f"- {func['name']} -> @keyword")