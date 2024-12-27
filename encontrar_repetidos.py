import os
from collections import defaultdict
from var import *

def find_duplicates(start_dir, ignore_files, amount_repeat, min_file_length):
    # Dicionário para armazenar os arquivos por nome e tamanho
    files_by_name = defaultdict(list)

    # Caminha pela árvore de diretórios
    for dirpath, _, filenames in os.walk(start_dir):
        for filename in filenames:
            # Ignora arquivos especificados
            if filename in ignore_files or filename.endswith(ignore_extensions):
                continue
            
            filepath = os.path.join(dirpath, filename)
            file_size = os.path.getsize(filepath)

            # Armazena o arquivo com base no nome e tamanho
            files_by_name[(filename, file_size)].append(filepath)

    # Filtra os arquivos duplicados
    duplicates = [(files, size) for (name, size), files in files_by_name.items() if len(files) >= amount_repeat and size > min_file_length]

    return duplicates

def converter_bytes(bytes):
    
    unidades = ["Bytes", "KB", "MB", "GB", "TB"]
    fator = 1024.0
    indice = 0

    while bytes >= fator and indice < len(unidades) - 1:
        bytes /= fator
        indice += 1

    return f"{bytes:.2f} {unidades[indice]}"


def save_results(duplicates, output_file):
    """Salva os resultados em um arquivo de texto."""
    resultados = []
    tamanho_final = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Total de arquivos: {len(duplicates)}\n\n")
        for files, size in sorted(duplicates, key=lambda x: x[1], reverse=True):
            for file in files:
                # Salva apenas o nome do arquivo
                # print(size)
                resultado = f"{os.path.basename(file)} - {converter_bytes(size)}"
                if resultado not in resultados:
                    f.write(f"{resultado}\n")
                    tamanho_final += size
                    resultados.append(resultado)

    return tamanho_final

if __name__ == "__main__":
    # start_directory = os.getcwd()  # Diretório atual onde o script é executado
    start_directory = SEARCH_PATH
    ignore_files = IGNORE_FILES 
    ignore_extensions = IGNORE_EXTENSIONS
    amount_repeat = AMOUNT_REPEAT
    min_file_length = MIN_FILE_LENGTH
    duplicates = find_duplicates(start_directory, ignore_files, amount_repeat, min_file_length) 

    if duplicates:
        output_filename = 'repetidos.txt'
        tamanho_final = save_results(duplicates, output_filename)
        print(f"Resultados salvos em '{output_filename}'")
        print(f"Tamanho dos arquivos: {converter_bytes(tamanho_final)}")
    else:
        print("Nenhum arquivo duplicado encontrado.")
