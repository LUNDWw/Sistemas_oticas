def safe_int(value, default=0):
    try:
        return int(value) if value else default
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    try:
        return float(value) if value else default
    except (ValueError, TypeError):
        return default


def validate_amount(value, allow_zero=False):
    """
    Valida um valor monetário
    
    Args:
        value: Valor a ser validado
        allow_zero: Se True, permite valores zero
        
    Returns:
        tuple: (sucesso: bool, valor: float, erro: str)
    """
    amount = safe_float(value)
    
    if value is None or str(value).strip() == '':
        return False, 0.0, "Valor é obrigatório"
    
    if amount <= 0 and not allow_zero:
        return False, 0.0, "Valor deve ser maior que zero"
    
    if amount < 0:
        return False, 0.0, "Valor não pode ser negativo"
    
    # Limitar a 2 casas decimais (padrão monetário)
    amount = round(amount, 2)
    
    return True, amount, ""


def validate_date(date_str):
    """
    Valida uma data no formato YYYY-MM-DD
    
    Args:
        date_str: String de data
        
    Returns:
        tuple: (válida: bool, erro: str)
    """
    if not date_str or not isinstance(date_str, str):
        return False, "Data é obrigatória"
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, "Data deve estar no formato YYYY-MM-DD"


def is_safe_redirect(url, request_host):
    """
    Valida se uma URL de redirecionamento é segura (mesmo domínio)
    Protege contra Open Redirect vulnerabilities
    
    Args:
        url: URL para redirecionar
        request_host: Host do request (request.host)
        
    Returns:
        bool: True se seguro, False caso contrário
    """
    if not url:
        return False
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        
        # URLs relativas são seguras
        if not parsed.netloc:
            return True
        
        # URLs com domínio diferente são inseguras
        if parsed.netloc != request_host:
            return False
        
        # URLs com mesmo domínio são seguras
        return True
    except Exception:
        return False


def soft_delete_order(db, order_id):
    """
    Executa soft-delete em uma ordem (marca como deletada, não remove)
    
    Args:
        db: Conexão do banco de dados
        order_id: ID da ordem a deletar
        
    Returns:
        bool: True se deletada com sucesso, False caso contrário
    """
    try:
        from datetime import datetime
        deleted_at = datetime.now().isoformat()
        
        db.execute(
            "UPDATE orders SET deleted_at = ? WHERE id = ?",
            (deleted_at, order_id)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao fazer soft-delete de ordem: {e}")
        return False


def restore_order(db, order_id):
    """
    Restaura uma ordem deletada (soft-delete)
    
    Args:
        db: Conexão do banco de dados
        order_id: ID da ordem a restaurar
        
    Returns:
        bool: True se restaurada com sucesso, False caso contrário
    """
    try:
        db.execute(
            "UPDATE orders SET deleted_at = NULL WHERE id = ?",
            (order_id,)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao restaurar ordem: {e}")
        return False
