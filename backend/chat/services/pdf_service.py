from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io
from typing import List, Dict

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.blue
        )

    def generate_learning_report(self, session_data: Dict):
        """Genera un reporte PDF completo de la sesión de aprendizaje"""
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        session_info = session_data.get('session_info', {})
        concepts = session_data.get('concepts_covered', [])
        exercises = session_data.get('exercises_completed', [])
        questions = session_data.get('questions_asked', [])
        history = session_data.get('session_history', [])
        
        title = Paragraph(f"Reporte de Aprendizaje - {session_info.get('topic', 'Matemáticas')}", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        session_info_data = [
            ["Usuario:", session_info.get('user_id', 'N/A')],
            ["Tema:", session_info.get('topic', 'N/A')],
            ["Subtema:", session_info.get('subtopic', 'N/A') or 'General'],
            ["Nivel:", session_info.get('level', 'N/A')],
            ["Estado:", session_info.get('status', 'N/A')],
            ["Fecha de inicio:", self._format_datetime(session_info.get('created_at'))],
            ["Último acceso:", self._format_datetime(session_info.get('last_accessed'))],
            ["Duración total:", self._calculate_duration(session_info)],
        ]
        
        session_table = Table(session_info_data, colWidths=[2*inch, 4*inch])
        session_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(session_table)
        story.append(Spacer(1, 20))
        
        stats_title = Paragraph("Resumen de Progreso", self.heading_style)
        story.append(stats_title)
        
        total_exercises = len(exercises)
        correct_exercises = sum(1 for ex in exercises if ex.get('is_correct', False))
        accuracy = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        stats_data = [
            ["Conceptos aprendidos:", str(len(concepts))],
            ["Ejercicios completados:", str(total_exercises)],
            ["Respuestas correctas:", str(correct_exercises)],
            ["Precisión:", f"{accuracy:.1f}%"],
            ["Preguntas libres:", str(len(questions))],
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        if concepts:
            concepts_title = Paragraph("Conceptos Aprendidos", self.heading_style)
            story.append(concepts_title)
            
            for i, concept in enumerate(concepts, 1):
                concept_text = Paragraph(f"{i}. {concept}", self.styles['Normal'])
                story.append(concept_text)
            story.append(Spacer(1, 20))
        
        if exercises:
            exercises_title = Paragraph("Ejercicios Realizados", self.heading_style)
            story.append(exercises_title)
            
            for i, exercise in enumerate(exercises, 1):
                status = "✓ Correcto" if exercise.get('is_correct') else "✗ Incorrecto"
                exercise_text = Paragraph(
                    f"{i}. <b>Pregunta:</b> {exercise.get('question', 'N/A')[:100]}...<br/>"
                    f"<b>Tu respuesta:</b> {exercise.get('user_answer', 'N/A')}<br/>"
                    f"<b>Respuesta correcta:</b> {exercise.get('correct_answer', 'N/A')}<br/>"
                    f"<b>Estado:</b> {status}<br/><br/>",
                    self.styles['Normal']
                )
                story.append(exercise_text)
            story.append(Spacer(1, 20))
        
        if questions:
            questions_title = Paragraph("Preguntas Realizadas", self.heading_style)
            story.append(questions_title)
            
            for i, question in enumerate(questions, 1):
                question_text = Paragraph(
                    f"{i}. <b>Pregunta:</b> {question.get('question', 'N/A')}<br/>"
                    f"<b>Respuesta:</b> {question.get('answer', 'N/A')[:200]}...<br/>"
                    f"<b>Fecha:</b> {self._format_datetime(question.get('asked_at'))}<br/><br/>",
                    self.styles['Normal']
                )
                story.append(question_text)
            story.append(Spacer(1, 20))
        
        # Cronología de aprendizaje
        if history:
            history_title = Paragraph("Cronología de Aprendizaje", self.heading_style)
            story.append(history_title)
            
            # Limitar a las últimas 10 interacciones para no hacer el PDF muy largo
            recent_history = sorted(history, key=lambda x: x.get('timestamp', datetime.min), reverse=True)[:10]
            
            for item in recent_history:
                interaction_type = item.get('type', 'unknown')
                content = item.get('content', 'N/A')
                timestamp = self._format_datetime(item.get('timestamp'))
                
                type_emoji = {
                    'question': '❓',
                    'explanation': '📚',
                    'exercise': '📝',
                    'answer': '💬',
                    'concept': '🎯'
                }.get(interaction_type, '📌')
                
                history_text = Paragraph(
                    f"{type_emoji} <b>{timestamp}</b> - {interaction_type.title()}<br/>"
                    f"{content[:150]}{'...' if len(content) > 150 else ''}<br/><br/>",
                    self.styles['Normal']
                )
                story.append(history_text)
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _calculate_duration(self, session_data: Dict) -> str:
        """Calcula la duración de la sesión"""
        if 'created_at' in session_data and 'last_accessed' in session_data:
            created_at = session_data['created_at']
            last_accessed = session_data['last_accessed']
            if created_at and last_accessed:
                duration = last_accessed - created_at
                hours = int(duration.total_seconds() // 3600)
                minutes = int((duration.total_seconds() % 3600) // 60)
                if hours > 0:
                    return f"{hours}h {minutes}min"
                else:
                    return f"{minutes} minutos"
        return "N/A"

    def _format_datetime(self, dt) -> str:
        """Formatea una fecha/hora para mostrar en el PDF"""
        if dt:
            return dt.strftime("%d/%m/%Y %H:%M")
        return "N/A"

    def generate_exercises_pdf(self, session_data: Dict, exercises_only: bool = True):
        """Genera un PDF solo con los ejercicios de una sesión"""
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        session_info = session_data.get('session_info', {})
        exercises = session_data.get('exercises_completed', [])
        
        # Título
        title = Paragraph(f"Ejercicios - {session_info.get('topic', 'Matemáticas')}", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Información básica de la sesión
        basic_info = [
            ["Tema:", session_info.get('topic', 'N/A')],
            ["Subtema:", session_info.get('subtopic', 'N/A') or 'General'],
            ["Total de ejercicios:", str(len(exercises))],
            ["Fecha:", self._format_datetime(session_info.get('created_at'))],
        ]
        
        info_table = Table(basic_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Lista de ejercicios
        if exercises:
            exercises_title = Paragraph("Lista de Ejercicios Completados", self.heading_style)
            story.append(exercises_title)
            
            for i, exercise in enumerate(exercises, 1):
                status = "✓ Correcto" if exercise.get('is_correct') else "✗ Incorrecto"
                difficulty = exercise.get('difficulty', 'N/A')
                
                exercise_content = [
                    f"<b>Ejercicio {i}</b>",
                    f"<b>Dificultad:</b> {difficulty}",
                    f"<b>Pregunta:</b>",
                    exercise.get('question', 'N/A'),
                    "",
                    f"<b>Tu respuesta:</b> {exercise.get('user_answer', 'N/A')}",
                    f"<b>Respuesta correcta:</b> {exercise.get('correct_answer', 'N/A')}",
                    f"<b>Estado:</b> {status}",
                    ""
                ]
                
                exercise_text = Paragraph("<br/>".join(exercise_content), self.styles['Normal'])
                story.append(exercise_text)
                story.append(Spacer(1, 15))
        else:
            no_exercises = Paragraph("No hay ejercicios completados en esta sesión.", self.styles['Normal'])
            story.append(no_exercises)
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

pdf_service = PDFService()
