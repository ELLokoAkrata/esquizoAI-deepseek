import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import math
import random
from typing import Dict, List, Tuple
import os
from datetime import datetime
import json

class VisionaryArtGenerator:
    def __init__(self):
        self.output_dir = "generated_art"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Paletas de colores visionarias
        self.color_palettes = {
            "psychedelic": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF6600", "#9900FF"],
            "cosmic": ["#000033", "#000066", "#003366", "#006699", "#0099CC", "#00CCFF"],
            "sacred": ["#FFD700", "#FF8C00", "#DC143C", "#8B0000", "#4B0082"],
            "jungle": ["#228B22", "#32CD32", "#ADFF2F", "#7FFF00", "#00FF7F"],
            "fire": ["#FF0000", "#FF4500", "#FFA500", "#FFD700", "#FFFF00"],
            "water": ["#000080", "#0000CD", "#4169E1", "#1E90FF", "#87CEEB"],
            "earth": ["#8B4513", "#A0522D", "#CD853F", "#DEB887", "#F5DEB3"]
        }
        
    def mandala_generator(self, complexity: int = 8, palette: str = "psychedelic", 
                         size: Tuple[int, int] = (800, 800)) -> str:
        """Genera un mandala geométrico visionario"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        colors = self.color_palettes[palette]
        center = (0, 0)
        
        # Círculos concéntricos
        for i in range(complexity):
            radius = 0.9 - (i * 0.1)
            circle = plt.Circle(center, radius, fill=False, 
                              color=colors[i % len(colors)], 
                              linewidth=2, alpha=0.7)
            ax.add_patch(circle)
            
        # Patrones radiales
        num_rays = complexity * 4
        for i in range(num_rays):
            angle = (2 * math.pi * i) / num_rays
            x1, y1 = 0.1 * math.cos(angle), 0.1 * math.sin(angle)
            x2, y2 = 0.9 * math.cos(angle), 0.9 * math.sin(angle)
            ax.plot([x1, x2], [y1, y2], 
                   color=colors[i % len(colors)], 
                   linewidth=1, alpha=0.6)
        
        # Formas geométricas
        for layer in range(3):
            num_shapes = 6 + layer * 2
            radius_pos = 0.3 + layer * 0.2
            
            for i in range(num_shapes):
                angle = (2 * math.pi * i) / num_shapes
                x = radius_pos * math.cos(angle)
                y = radius_pos * math.sin(angle)
                
                if layer % 2 == 0:
                    # Triángulos
                    triangle_size = 0.05
                    triangle = patches.RegularPolygon((x, y), 3, triangle_size,
                                                    orientation=angle,
                                                    facecolor=colors[(i + layer) % len(colors)],
                                                    alpha=0.8)
                    ax.add_patch(triangle)
                else:
                    # Círculos pequeños
                    small_circle = plt.Circle((x, y), 0.03,
                                            facecolor=colors[(i + layer) % len(colors)],
                                            alpha=0.9)
                    ax.add_patch(small_circle)
        
        filename = f"mandala_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        return filepath

    def fractal_geometry(self, pattern_type: str = "sierpinski", 
                        iterations: int = 5, palette: str = "cosmic",
                        size: Tuple[int, int] = (800, 800)) -> str:
        """Genera geometría fractal visionaria"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        colors = self.color_palettes[palette]
        
        if pattern_type == "sierpinski":
            self._draw_sierpinski(ax, iterations, colors)
        elif pattern_type == "dragon":
            self._draw_dragon_curve(ax, iterations, colors)
        elif pattern_type == "tree":
            self._draw_fractal_tree(ax, iterations, colors)
        
        filename = f"fractal_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        return filepath

    def sacred_geometry(self, pattern: str = "flower_of_life", 
                       palette: str = "sacred",
                       size: Tuple[int, int] = (800, 800)) -> str:
        """Genera patrones de geometría sagrada"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        colors = self.color_palettes[palette]
        
        if pattern == "flower_of_life":
            self._draw_flower_of_life(ax, colors)
        elif pattern == "metatron":
            self._draw_metatron_cube(ax, colors)
        elif pattern == "sri_yantra":
            self._draw_sri_yantra(ax, colors)
        
        filename = f"sacred_{pattern}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        return filepath

    def psychedelic_wave(self, wave_type: str = "interference", 
                        palette: str = "psychedelic",
                        size: Tuple[int, int] = (800, 800)) -> str:
        """Genera patrones de ondas psicodélicas"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        x = np.linspace(-4*np.pi, 4*np.pi, 400)
        y = np.linspace(-4*np.pi, 4*np.pi, 400)
        X, Y = np.meshgrid(x, y)
        
        if wave_type == "interference":
            Z = np.sin(np.sqrt(X**2 + Y**2)) * np.cos(X) * np.sin(Y)
        elif wave_type == "ripple":
            Z = np.sin(np.sqrt(X**2 + Y**2)) / (np.sqrt(X**2 + Y**2) + 0.1)
        elif wave_type == "spiral":
            Z = np.sin(np.arctan2(Y, X) * 5 + np.sqrt(X**2 + Y**2))
        
        colors_list = self.color_palettes[palette]
        cmap = LinearSegmentedColormap.from_list("visionario", colors_list)
        
        ax.contourf(X, Y, Z, levels=20, cmap=cmap, alpha=0.8)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        filename = f"wave_{wave_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        return filepath

    def _draw_sierpinski(self, ax, iterations, colors):
        """Triángulo de Sierpinski"""
        vertices = [(0, 0), (1, 0), (0.5, np.sqrt(3)/2)]
        
        def sierpinski(vertices, depth, color_idx):
            if depth == 0:
                triangle = plt.Polygon(vertices, facecolor=colors[color_idx % len(colors)], 
                                     edgecolor='white', alpha=0.7, linewidth=0.5)
                ax.add_patch(triangle)
                return
            
            # Puntos medios
            mid1 = ((vertices[0][0] + vertices[1][0])/2, (vertices[0][1] + vertices[1][1])/2)
            mid2 = ((vertices[1][0] + vertices[2][0])/2, (vertices[1][1] + vertices[2][1])/2)
            mid3 = ((vertices[2][0] + vertices[0][0])/2, (vertices[2][1] + vertices[0][1])/2)
            
            sierpinski([vertices[0], mid1, mid3], depth-1, color_idx+1)
            sierpinski([mid1, vertices[1], mid2], depth-1, color_idx+2)
            sierpinski([mid3, mid2, vertices[2]], depth-1, color_idx+3)
        
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1)
        sierpinski(vertices, iterations, 0)

    def _draw_flower_of_life(self, ax, colors):
        """Flor de la Vida"""
        radius = 0.5
        centers = [(0, 0)]
        
        # Primera corona
        for i in range(6):
            angle = i * np.pi / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            centers.append((x, y))
        
        # Segunda corona
        for i in range(6):
            angle = i * np.pi / 3
            for j in range(2):
                if j == 0:
                    r = radius * np.sqrt(3)
                    x = r * np.cos(angle)
                    y = r * np.sin(angle)
                else:
                    r = radius * np.sqrt(3)
                    angle_offset = np.pi / 6
                    x = r * np.cos(angle + angle_offset)
                    y = r * np.sin(angle + angle_offset)
                centers.append((x, y))
        
        for i, center in enumerate(centers):
            circle = plt.Circle(center, radius, fill=False, 
                              color=colors[i % len(colors)], 
                              linewidth=2, alpha=0.8)
            ax.add_patch(circle)

    def _draw_fractal_tree(self, ax, iterations, colors):
        """Árbol fractal"""
        def draw_branch(x1, y1, angle, length, depth):
            if depth == 0:
                return
            
            x2 = x1 + length * np.cos(angle)
            y2 = y1 + length * np.sin(angle)
            
            ax.plot([x1, x2], [y1, y2], 
                   color=colors[depth % len(colors)], 
                   linewidth=depth, alpha=0.8)
            
            # Ramas
            new_length = length * 0.7
            draw_branch(x2, y2, angle - np.pi/6, new_length, depth-1)
            draw_branch(x2, y2, angle + np.pi/6, new_length, depth-1)
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        draw_branch(0, -1.5, np.pi/2, 1, iterations)

    def _draw_metatron_cube(self, ax, colors):
        """Cubo de Metatrón"""
        # Círculo de círculos
        radius = 0.3
        centers = [(0, 0)]
        
        # Corona de 6 círculos
        for i in range(6):
            angle = i * np.pi / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            centers.append((x, y))
        
        # Segunda corona
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x = radius * 2 * np.cos(angle)
            y = radius * 2 * np.sin(angle)
            centers.append((x, y))
        
        # Dibujar círculos
        for i, center in enumerate(centers):
            circle = plt.Circle(center, 0.1, fill=False, 
                              color=colors[i % len(colors)], 
                              linewidth=2, alpha=0.8)
            ax.add_patch(circle)
        
        # Conectar con líneas
        for i, center1 in enumerate(centers):
            for j, center2 in enumerate(centers[i+1:], i+1):
                ax.plot([center1[0], center2[0]], [center1[1], center2[1]], 
                       color=colors[(i+j) % len(colors)], 
                       linewidth=0.5, alpha=0.6)

    def _draw_sri_yantra(self, ax, colors):
        """Sri Yantra simplificado"""
        # Triángulos ascendentes y descendentes
        for i in range(4):
            size = 1.5 - i * 0.3
            # Triángulo ascendente
            triangle_up = patches.RegularPolygon((0, 0), 3, size,
                                               orientation=0,
                                               facecolor='none',
                                               edgecolor=colors[i % len(colors)],
                                               linewidth=2, alpha=0.8)
            ax.add_patch(triangle_up)
            
            # Triángulo descendente
            triangle_down = patches.RegularPolygon((0, 0), 3, size * 0.8,
                                                 orientation=np.pi,
                                                 facecolor='none',
                                                 edgecolor=colors[(i+2) % len(colors)],
                                                 linewidth=2, alpha=0.8)
            ax.add_patch(triangle_down)

    def yin_yang_generator(self, colors: List[str] = None, style: str = "classic", 
                          size: Tuple[int, int] = (800, 800)) -> str:
        """Genera el símbolo del Yin-Yang con un toque visionario"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        # Colores por defecto
        if colors is None:
            colors = ["#FFFFFF", "#000000"]
        
        # Círculo exterior
        circle = plt.Circle((0, 0), 0.9, color=colors[0], ec="none")
        ax.add_patch(circle)
        
        # Semicírculos
        for i in [-1, 1]:
            semi_circle = patches.Arc((0, 0), 1.8, 1.8, 0, 0, 180, 
                                    color=colors[i % 2], linewidth=2, alpha=0.9)
            ax.add_patch(semi_circle)
        
        # Círculos internos
        for i in [-1, 1]:
            small_circle = plt.Circle((i * 0.35, 0), 0.15, color=colors[i % 2], ec="none")
            ax.add_patch(small_circle)
        
        # Punto central
        center_circle = plt.Circle((0, 0), 0.1, color=colors[1], ec="none")
        ax.add_patch(center_circle)
        
        # Estilo cósmico (opcional)
        if style == "cosmic":
            for i in range(10):
                r = 0.9 - i * 0.08
                cosmic_circle = plt.Circle((0, 0), r, color=colors[i % 2], fill=False, 
                                          linewidth=1, alpha=0.3)
                ax.add_patch(cosmic_circle)
        
        filename = f"yin_yang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        return filepath

# Función principal para crear arte visionario geométrico (ACTUALIZADA)
def create_visionary_art(art_type: str, **kwargs) -> Dict:
    """
    Función principal para crear arte visionario geométrico
    
    Args:
        art_type: Tipo de arte ('mandala', 'fractal', 'sacred', 'wave', 'yin_yang')
        **kwargs: Parámetros específicos para cada tipo
    
    Returns:
        Dict con información del archivo creado
    """
    generator = VisionaryArtGenerator()
    
    try:
        if art_type == "mandala":
            filepath = generator.mandala_generator(
                complexity=kwargs.get('complexity', 8),
                palette=kwargs.get('palette', 'psychedelic'),
                size=kwargs.get('size', (800, 800))
            )
        elif art_type == "fractal":
            filepath = generator.fractal_geometry(
                pattern_type=kwargs.get('pattern', 'sierpinski'),
                iterations=kwargs.get('iterations', 5),
                palette=kwargs.get('palette', 'cosmic'),
                size=kwargs.get('size', (800, 800))
            )
        elif art_type == "sacred":
            filepath = generator.sacred_geometry(
                pattern=kwargs.get('pattern', 'flower_of_life'),
                palette=kwargs.get('palette', 'sacred'),
                size=kwargs.get('size', (800, 800))
            )
        elif art_type == "wave":
            filepath = generator.psychedelic_wave(
                wave_type=kwargs.get('wave_type', 'interference'),
                palette=kwargs.get('palette', 'psychedelic'),
                size=kwargs.get('size', (800, 800))
            )
        elif art_type == "yin_yang":
            # ✅ NUEVO: Yin-Yang con colores personalizables
            filepath = generator.yin_yang_generator(
                colors=kwargs.get('colors', None),
                style=kwargs.get('style', 'classic'),
                size=kwargs.get('size', (800, 800))
            )
        else:
            return {"error": f"Tipo de arte no reconocido: {art_type}"}
        
        return {
            "success": True,
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "type": art_type,
            "parameters": kwargs
        }
        
    except Exception as e:
        return {"error": f"Error creando arte: {str(e)}"}

# Función tools para DeepSeek (ACTUALIZADA)
VISIONARY_ART_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_visionary_art",
            "description": "Crea arte visionario geométrico en diferentes estilos usando Python y matemáticas",
            "parameters": {
                "type": "object",
                "properties": {
                    "art_type": {
                        "type": "string",
                        "enum": ["mandala", "fractal", "sacred", "wave", "yin_yang"],
                        "description": "Tipo de arte a crear"
                    },
                    "complexity": {
                        "type": "integer",
                        "minimum": 3,
                        "maximum": 12,
                        "description": "Complejidad del patrón (solo para mandala)"
                    },
                    "pattern": {
                        "type": "string", 
                        "description": "Patrón específico (fractal: sierpinski/dragon/tree, sacred: flower_of_life/metatron/sri_yantra)"
                    },
                    "wave_type": {
                        "type": "string",
                        "enum": ["interference", "ripple", "spiral"],
                        "description": "Tipo de onda (solo para wave)"
                    },
                    "palette": {
                        "type": "string",
                        "enum": ["psychedelic", "cosmic", "sacred", "jungle", "fire", "water", "earth"],
                        "description": "Paleta de colores (no aplica a yin_yang)"
                    },
                    "iterations": {
                        "type": "integer",
                        "minimum": 3,
                        "maximum": 8,
                        "description": "Número de iteraciones (solo para fractal)"
                    },
                    "colors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de colores en formato hex (solo para yin_yang). Ej: ['#FF0000', '#00FF00']"
                    },
                    "style": {
                        "type": "string",
                        "enum": ["classic", "cosmic", "elemental", "chakra"],
                        "description": "Estilo del Yin-Yang (solo para yin_yang)"
                    }
                },
                "required": ["art_type"]
            }
        }
    }
]
