import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from app.models import get_db
from app.utils import safe_int, safe_float, validate_amount, validate_date
from app.services import order_service

order_bp = Blueprint('order', __name__)

@order_bp.route('/new', methods=['GET','POST'])
def new_order():
    db = get_db()
    if request.method == 'POST':
        try:
            # Validar amounts
            valid_pago, valor_pago, error_pago = validate_amount(request.form.get('valor_pago'))
            if not valid_pago:
                flash(f'Valor Pago inválido: {error_pago}', 'error')
                return redirect(url_for('order.new_order'))
            
            valid_entrada, entrada, error_entrada = validate_amount(request.form.get('entrada'), allow_zero=True)
            if not valid_entrada:
                flash(f'Entrada inválida: {error_entrada}', 'error')
                return redirect(url_for('order.new_order'))
            
            # Validar datas se fornecidas
            exam_date = request.form.get('exam_date', '')
            if exam_date:
                valid_exam, error_exam = validate_date(exam_date)
                if not valid_exam:
                    flash(f'Data do Exame inválida: {error_exam}', 'error')
                    return redirect(url_for('order.new_order'))
            
            delivery_date = request.form.get('delivery_date', '')
            if delivery_date:
                valid_delivery, error_delivery = validate_date(delivery_date)
                if not valid_delivery:
                    flash(f'Data de Entrega inválida: {error_delivery}', 'error')
                    return redirect(url_for('order.new_order'))
            
            # Validar campos obrigatórios
            if not request.form.get('os_number', '').strip():
                flash('Número da OS é obrigatório', 'error')
                return redirect(url_for('order.new_order'))
            
            if not request.form.get('client_name', '').strip():
                flash('Nome do Cliente é obrigatório', 'error')
                return redirect(url_for('order.new_order'))
            
            receita_fora = 1 if request.form.get('receita_fora') == 'on' else 0
            pagamento_retirada = 1 if request.form.get('pagamento_retirada') == 'on' else 0
            valor_retirada = safe_float(request.form.get('valor_retirada')) if pagamento_retirada else 0.0
            
            data = (
                request.form.get('os_number','').strip(),
                request.form.get('client_name','').strip(),
                request.form.get('phone','').strip(),
                request.form.get('purchase_type',''),
                request.form.get('store',''),
                request.form.get('lab',''),
                request.form.get('payment_status',''),
                request.form.get('payment_method',''),
                safe_int(request.form.get('installments','0')),
                1 if request.form.get('lab_paid') == 'on' else 0,
                exam_date,
                delivery_date,
                request.form.get('cpf','').strip(),
                receita_fora,
                request.form.get('nome_doutor_fora','').strip(),
                valor_pago,
                entrada,
                valor_retirada,
                request.form.get('nome_doutor_otica','').strip(),
                request.form.get('endereco','').strip()
            )
            order_service.create_order(db, data)
            flash('Ordem criada com sucesso.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Erro ao criar ordem: {str(e)}', 'error')
            return redirect(url_for('order.new_order'))
    
    return render_template('form_full.html', action="Criar", order=None, graus=None)

@order_bp.route('/edit/<int:order_id>', methods=['GET','POST'])
def edit_order(order_id):
    db = get_db()
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        flash('Ordem não encontrada.', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        try:
            receita_fora = 1 if request.form.get('receita_fora') == 'on' else 0
            pagamento_retirada = 1 if request.form.get('pagamento_retirada') == 'on' else 0
            valor_retirada = safe_float(request.form.get('valor_retirada')) if pagamento_retirada else 0.0
            
            # Use safe variables for safe execution
            q_installments = safe_int(request.form.get('installments','0'))
            q_pago = safe_float(request.form.get('valor_pago'))
            q_entrada = safe_float(request.form.get('entrada'))
            data = (
                request.form.get('os_number',''),
                request.form.get('client_name',''),
                request.form.get('phone',''),
                request.form.get('purchase_type',''),
                request.form.get('store',''),
                request.form.get('lab',''),
                request.form.get('payment_status',''),
                request.form.get('payment_method',''),
                q_installments,
                1 if request.form.get('lab_paid') == 'on' else 0,
                request.form.get('exam_date',''),
                request.form.get('delivery_date',''),
                request.form.get('cpf',''),
                receita_fora,
                request.form.get('nome_doutor_fora',''),
                q_pago,
                q_entrada,
                valor_retirada,
                request.form.get('nome_doutor_otica',''),
                request.form.get('endereco','')
            )
            order_service.update_order(db, order_id, data)
            flash('Ordem atualizada com sucesso.', 'success')
        except Exception as e:
            flash(f'Erro ao atualizar ordem: {str(e)}', 'danger')
        return redirect(url_for('order.edit_order', order_id=order_id))
    graus = order_service.get_graus_for_order(db, order_id)
    return render_template('form_full.html', action="Editar", order=order, graus=graus)

@order_bp.route('/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    db = get_db()
    
    # Verificar se a ordem existe
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        flash('Ordem não encontrada.', 'danger')
        return redirect(url_for('main.index'))
    
    # Usar soft-delete
    if order_service.soft_delete_order(db, order_id):
        flash('Ordem excluída com sucesso.', 'success')
    else:
        flash('Erro ao excluir ordem.', 'danger')
    
    return redirect(url_for('main.index'))


@order_bp.route('/order/<int:order_id>/grau/new', methods=['POST'])
def new_grau(order_id):
    db = get_db()
    try:
        data = (
            order_id,
            request.form.get('lens_for',''),
            request.form.get('eye',''),
            request.form.get('esf',''),
            request.form.get('cil',''),
            request.form.get('eixo',''),
            request.form.get('dnp',''),
            request.form.get('indice',''),
            request.form.get('lens_type',''),
            request.form.get('adicao','')
        )
        order_service.add_grau(db, data)
        flash('Grau adicionado.', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar grau: {str(e)}', 'danger')
    return redirect(url_for('order.edit_order', order_id=order_id))

@order_bp.route('/order/<int:order_id>/grau/json/<int:grau_id>')
def grau_json(order_id, grau_id):
    db = get_db()
    grau = order_service.get_grau_by_id(db, order_id, grau_id)
    if not grau:
        return jsonify({'error': 'not found'}), 404
    return jsonify({k: grau[k] for k in grau.keys()})

@order_bp.route('/order/<int:order_id>/grau/edit/<int:grau_id>', methods=['POST'])
def edit_grau(order_id, grau_id):
    db = get_db()
    grau = order_service.get_grau_by_id(db, order_id, grau_id)
    if not grau:
        flash('Grau não encontrado.', 'danger')
        return redirect(url_for('order.edit_order', order_id=order_id))
    try:
        data = (
            request.form.get('lens_for',''),
            request.form.get('eye',''),
            request.form.get('esf',''),
            request.form.get('cil',''),
            request.form.get('eixo',''),
            request.form.get('dnp',''),
            request.form.get('indice',''),
            request.form.get('lens_type',''),
            request.form.get('adicao','')
        )
        order_service.update_grau(db, grau_id, data)
        flash('Grau atualizado.', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar grau: {str(e)}', 'danger')
    return redirect(url_for('order.edit_order', order_id=order_id))

@order_bp.route('/order/<int:order_id>/grau/delete/<int:grau_id>', methods=['POST'])
def delete_grau(order_id, grau_id):
    db = get_db()
    order_service.delete_grau(db, order_id, grau_id)
    flash('Grau excluído.', 'success')
    return redirect(url_for('order.edit_order', order_id=order_id))

@order_bp.route('/details/<int:order_id>')
def details(order_id):
    db = get_db()
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        flash('Ordem não encontrada.', 'danger')
        return redirect(url_for('main.index'))
    graus = order_service.get_graus_for_order(db, order_id)
    
    # Get partial payments
    partial_payments = order_service.get_partial_payments(db, order_id)
    
    # Calculate total paid
    total_paid = order_service.get_total_paid(db, order_id)
    
    return render_template('details.html', order=order, graus=graus, 
                         partial_payments=partial_payments, total_paid=total_paid)

@order_bp.route('/details/<int:order_id>/download')
def download_order(order_id):
    db = get_db()
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        flash('Ordem não encontrada.', 'danger')
        return redirect(url_for('main.index'))
    
    graus = order_service.get_graus_for_order(db, order_id)
    order_dict = {k: order[k] for k in order.keys()}
    graus_list = [{k: g[k] for k in g.keys()} for g in graus]
    payload = {'order': order_dict, 'graus': graus_list}

    # Validar formato solicitado
    VALID_FORMATS = {'txt', 'json'}
    fmt = request.args.get('format', 'json').lower().strip()
    
    if fmt not in VALID_FORMATS:
        fmt = 'json'  # Fallback para formato padrão
    
    if fmt == 'txt':
        lines = []
        lines.append(f"Ordem #{order_id}")
        lines.append("=== Dados da OS ===")
        for k, v in order_dict.items():
            lines.append(f"{k}: {v}")
        lines.append("\n=== Graus ===")
        for i, g in enumerate(graus_list, start=1):
            lines.append(f"Grau {i}:")
            for kk, vv in g.items():
                lines.append(f"  {kk}: {vv}")
            lines.append("")
        text = "\n".join(lines)
        resp = Response(text, mimetype='text/plain; charset=utf-8')
        resp.headers['Content-Disposition'] = f'attachment; filename=order_{order_id}.txt'
        return resp
    else:  # json
        data = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
        resp = Response(data, mimetype='application/json; charset=utf-8')
        resp.headers['Content-Disposition'] = f'attachment; filename=order_{order_id}.json'
        return resp
