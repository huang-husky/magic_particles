import pygame
import random
import math
import sys

pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Particles - 左键吸引 | 右键排斥 | 中键爆炸 | 双击烟花")
clock = pygame.time.Clock()

# 颜色
BG_COLOR = (10, 10, 30)

# 渐变色主题 - 扩展至15种
COLOR_THEMES = {
    # === 多色渐变系列 ===
    "1": {
        "name": "极光紫蓝",
        "colors": [(138, 43, 226), (75, 0, 130), (0, 191, 255), (30, 144, 255)]
    },
    "2": {
        "name": "烈焰橙红",
        "colors": [(255, 69, 0), (255, 140, 0), (255, 215, 0), (255, 99, 71)]
    },
    "3": {
        "name": "森林翠绿",
        "colors": [(0, 255, 127), (34, 139, 34), (144, 238, 144), (0, 250, 154)]
    },
    "4": {
        "name": "樱花粉白",
        "colors": [(255, 182, 193), (255, 105, 180), (255, 240, 245), (219, 112, 147)]
    },
    "5": {
        "name": "星空青金",
        "colors": [(0, 255, 255), (70, 130, 180), (255, 215, 0), (100, 149, 237)]
    },
    "6": {
        "name": "霓虹彩虹",
        "colors": [(255, 0, 128), (0, 255, 128), (128, 0, 255), (255, 128, 0)]
    },
    
    # === 单色深浅系列 ===
    "7": {
        "name": "深海蓝",
        "colors": [(0, 0, 139), (0, 0, 205), (65, 105, 225), (135, 206, 250), (173, 216, 230)]
    },
    "8": {
        "name": "烈焰红",
        "colors": [(139, 0, 0), (178, 34, 34), (220, 20, 60), (255, 69, 0), (255, 99, 71)]
    },
    "9": {
        "name": "翡翠绿",
        "colors": [(0, 100, 0), (34, 139, 34), (50, 205, 50), (144, 238, 144), (152, 251, 152)]
    },
    "10": {
        "name": "皇室紫",
        "colors": [(48, 0, 48), (75, 0, 130), (128, 0, 128), (186, 85, 211), (218, 112, 214)]
    },
    "11": {
        "name": "暖阳橙",
        "colors": [(255, 69, 0), (255, 99, 71), (255, 140, 0), (255, 165, 0), (255, 200, 100)]
    },
    "12": {
        "name": "冰晶青",
        "colors": [(0, 128, 128), (0, 206, 209), (64, 224, 208), (127, 255, 212), (175, 238, 238)]
    },
    
    # === 特殊配色系列 ===
    "13": {
        "name": "黑金尊贵",
        "colors": [(20, 20, 20), (40, 40, 40), (184, 134, 11), (218, 165, 32), (255, 215, 0)]
    },
    "14": {
        "name": "银白冰雪",
        "colors": [(192, 192, 192), (211, 211, 211), (220, 220, 220), (240, 248, 255), (255, 250, 250)]
    },
    "15": {
        "name": "日落黄昏",
        "colors": [(255, 94, 77), (255, 154, 0), (255, 206, 84), (255, 127, 80), (178, 34, 34)]
    },
    "16": {
        "name": "薰衣草梦",
        "colors": [(230, 230, 250), (216, 191, 216), (221, 160, 221), (238, 130, 238), (186, 85, 211)]
    },
    "17": {
        "name": "海洋珊瑚",
        "colors": [(0, 105, 148), (72, 209, 204), (255, 127, 80), (255, 160, 122), (240, 128, 128)]
    },
    "18": {
        "name": "糖果甜心",
        "colors": [(255, 182, 193), (255, 105, 180), (255, 0, 127), (138, 43, 226), (0, 191, 255)]
    },
}

# 获取用户输入
print("=" * 50)
print("        ✨ 魔幻粒子 Magic Particles ✨")
print("=" * 50)

while True:
    try:
        particle_count = int(input("\n请输入粒子数量 (50-2000): "))
        if 50 <= particle_count <= 2000:
            break
        print("请输入50到2000之间的数字！")
    except ValueError:
        print("请输入有效的数字！")

print("\n🎨 请选择颜色主题:\n")
print("  ══════ 多色渐变 ══════")
print("  [1] 极光紫蓝    [2] 烈焰橙红    [3] 森林翠绿")
print("  [4] 樱花粉白    [5] 星空青金    [6] 霓虹彩虹")
print("\n  ══════ 单色深浅 ══════")
print("  [7] 深海蓝      [8] 烈焰红      [9] 翡翠绿")
print("  [10] 皇室紫     [11] 暖阳橙     [12] 冰晶青")
print("\n  ══════ 特殊配色 ══════")
print("  [13] 黑金尊贵   [14] 银白冰雪   [15] 日落黄昏")
print("  [16] 薰衣草梦   [17] 海洋珊瑚   [18] 糖果甜心")

while True:
    choice = input("\n请输入选项 (1-18): ").strip()
    if choice in COLOR_THEMES:
        selected_theme = COLOR_THEMES[choice]
        break
    print("请输入1到18之间的数字！")

print(f"\n✅ 已选择: {selected_theme['name']}")


def clamp(value, min_val, max_val):
    """限制值在范围内"""
    return max(min_val, min(max_val, value))


class FireworkParticle:
    """烟花粒子"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(5, 15)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(0.015, 0.03)
        self.size = random.uniform(2, 4)
        self.gravity = 0.15
        self.trail = []
        self.max_trail = 5
        
    def update(self):
        self.trail.append({'x': self.x, 'y': self.y})
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= self.decay
        
    def draw(self, surface):
        if self.life <= 0:
            return
            
        alpha = clamp(int(self.life * 255), 0, 255)
        
        for i, point in enumerate(self.trail):
            if len(self.trail) == 0:
                continue
            t_alpha = clamp(int((i / len(self.trail)) * alpha * 0.5), 0, 255)
            t_size = max(1, int(self.size * (i / len(self.trail)) * 0.6))
            
            if t_size > 0 and t_alpha > 0:
                t_surface = pygame.Surface((t_size * 4, t_size * 4), pygame.SRCALPHA)
                draw_color = (
                    clamp(self.color[0], 0, 255),
                    clamp(self.color[1], 0, 255),
                    clamp(self.color[2], 0, 255),
                    t_alpha
                )
                pygame.draw.circle(t_surface, draw_color, (t_size * 2, t_size * 2), t_size)
                surface.blit(t_surface, (int(point['x'] - t_size * 2), int(point['y'] - t_size * 2)), special_flags=pygame.BLEND_RGBA_ADD)
        
        glow_size = int(self.size * 2)
        if glow_size > 0:
            glow_surface = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
            for r in range(glow_size * 2, 0, -1):
                a = clamp(int((r / (glow_size * 2)) * alpha * 0.4), 0, 255)
                draw_color = (
                    clamp(self.color[0], 0, 255),
                    clamp(self.color[1], 0, 255),
                    clamp(self.color[2], 0, 255),
                    a
                )
                pygame.draw.circle(glow_surface, draw_color, (glow_size * 2, glow_size * 2), r)
            surface.blit(glow_surface, (int(self.x - glow_size * 2), int(self.y - glow_size * 2)), special_flags=pygame.BLEND_RGBA_ADD)
        
        core_size = max(1, int(self.size * self.life))
        draw_color = (
            clamp(self.color[0], 0, 255),
            clamp(self.color[1], 0, 255),
            clamp(self.color[2], 0, 255),
            alpha
        )
        pygame.draw.circle(surface, draw_color, (int(self.x), int(self.y)), core_size)


class Particle:
    def __init__(self, theme_colors):
        self.theme_colors = theme_colors
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.size = random.uniform(0.3, 0.6)
        self.base_size = self.size
        self.color_index = random.uniform(0, len(theme_colors) - 1)
        self.color_speed = random.uniform(0.01, 0.03)
        self.alpha = random.randint(180, 255)
        self.pulse_offset = random.uniform(0, math.pi * 2)
        self.spin_vx = 0
        self.spin_vy = 0
        self.trail = []
        self.max_trail_length = 5
        
    def get_speed(self):
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)
        
    def update(self, mouse_pos, mouse_buttons, time, was_left_pressed, explosion_wave):
        speed = self.get_speed()
        if speed > 2:
            self.trail.append({
                'x': self.x, 
                'y': self.y, 
                'color': self.get_color(),
                'size': self.size
            })
            dynamic_max = min(int(speed * 1), self.max_trail_length)
            while len(self.trail) > dynamic_max:
                self.trail.pop(0)
        else:
            if self.trail:
                self.trail.pop(0)
        
        left_pressed, middle_pressed, right_pressed = mouse_buttons
        
        if explosion_wave:
            wave_x, wave_y, wave_radius, wave_force = explosion_wave
            dx = self.x - wave_x
            dy = self.y - wave_y
            distance = math.sqrt(dx * dx + dy * dy) + 0.1
            
            if abs(distance - wave_radius) < 60:
                force = wave_force * (1 - abs(distance - wave_radius) / 60)
                self.vx += (dx / distance) * force
                self.vy += (dy / distance) * force
        
        if was_left_pressed and not left_pressed:
            dx = self.x - mouse_pos[0]
            dy = self.y - mouse_pos[1]
            distance = math.sqrt(dx * dx + dy * dy) + 0.1
            
            if distance < 200:
                force = (200 - distance) / 200 * 15
                self.spin_vx = (dx / distance) * force
                self.spin_vy = (dy / distance) * force
                tangent_x = -dy / distance
                tangent_y = dx / distance
                spin_dir = 1 if random.random() > 0.5 else -1
                self.spin_vx += tangent_x * force * 0.6 * spin_dir
                self.spin_vy += tangent_y * force * 0.6 * spin_dir
        
        self.vx += self.spin_vx
        self.vy += self.spin_vy
        self.spin_vx *= 0.92
        self.spin_vy *= 0.92
        
        if (left_pressed or right_pressed) and mouse_pos:
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = math.sqrt(dx * dx + dy * dy) + 0.1
            
            if distance < 150:
                force = (150 - distance) / 150 * 0.8
                
                if left_pressed:
                    self.vx += (dx / distance) * force
                    self.vy += (dy / distance) * force
                elif right_pressed:
                    self.vx -= (dx / distance) * force * 1.5
                    self.vy -= (dy / distance) * force * 1.5
                
                self.size = self.base_size * (1 + (150 - distance) / 150)
            else:
                self.size = self.base_size
        else:
            self.size = self.base_size
        
        pulse = math.sin(time * 0.05 + self.pulse_offset)
        self.size *= (1 + pulse * 0.15)
        
        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.15, 0.15)
        self.vx *= 0.985
        self.vy *= 0.985
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0:
            self.x = 0
            self.vx *= -0.8
        elif self.x > WIDTH:
            self.x = WIDTH
            self.vx *= -0.8
        if self.y < 0:
            self.y = 0
            self.vy *= -0.8
        elif self.y > HEIGHT:
            self.y = HEIGHT
            self.vy *= -0.8
        
        self.color_index = (self.color_index + self.color_speed) % len(self.theme_colors)
    
    def get_color(self):
        idx = int(self.color_index)
        next_idx = (idx + 1) % len(self.theme_colors)
        t = self.color_index - idx
        
        c1 = self.theme_colors[idx]
        c2 = self.theme_colors[next_idx]
        
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        
        return (r, g, b)
    
    def draw(self, surface):
        color = self.get_color()
        
        if len(self.trail) > 1:
            for i, point in enumerate(self.trail):
                progress = i / len(self.trail)
                tail_alpha = int(progress * 100)
                tail_size = max(1, int(point['size'] * progress * 0.6))
                
                tail_surface = pygame.Surface((tail_size * 4, tail_size * 4), pygame.SRCALPHA)
                tail_color = point['color']
                
                for r in range(tail_size * 2, 0, -1):
                    a = int((r / (tail_size * 2)) * tail_alpha * 0.4)
                    pygame.draw.circle(tail_surface, (*tail_color, a), (tail_size * 2, tail_size * 2), r)
                
                surface.blit(tail_surface, 
                           (int(point['x'] - tail_size * 2), int(point['y'] - tail_size * 2)), 
                           special_flags=pygame.BLEND_RGBA_ADD)
        
        glow_size = int(self.size * 3)
        if glow_size > 1:
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for i in range(glow_size, 0, -1):
                alpha = int((i / glow_size) * 40)
                glow_color = (*color, alpha)
                pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), i)
            surface.blit(glow_surface, (int(self.x - glow_size), int(self.y - glow_size)), special_flags=pygame.BLEND_RGBA_ADD)
        
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.size)))


def draw_connections(surface, particles):
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            dx = particles[i].x - particles[j].x
            dy = particles[i].y - particles[j].y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 50:
                alpha = int((50 - distance) / 50 * 60)
                color1 = particles[i].get_color()
                color2 = particles[j].get_color()
                avg_color = (
                    (color1[0] + color2[0]) // 2,
                    (color1[1] + color2[1]) // 2,
                    (color1[2] + color2[2]) // 2
                )
                
                line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(line_surface, (*avg_color, alpha),
                               (int(particles[i].x), int(particles[i].y)),
                               (int(particles[j].x), int(particles[j].y)), 1)
                surface.blit(line_surface, (0, 0))


def draw_explosion_wave(surface, wave_x, wave_y, wave_radius, theme_colors):
    wave_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for i in range(3):
        r = wave_radius - i * 15
        if r > 0:
            alpha = max(0, 80 - int(wave_radius / 5))
            color = theme_colors[i % len(theme_colors)]
            pygame.draw.circle(wave_surface, (*color, alpha), (int(wave_x), int(wave_y)), int(r), 3)
    
    surface.blit(wave_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)


def create_firework(x, y, theme_colors):
    """创建烟花粒子"""
    firework_particles = []
    num_particles = random.randint(40, 60)
    
    for _ in range(num_particles):
        color = random.choice(theme_colors)
        color = (
            clamp(color[0] + random.randint(0, 50), 0, 255),
            clamp(color[1] + random.randint(0, 50), 0, 255),
            clamp(color[2] + random.randint(0, 50), 0, 255)
        )
        firework_particles.append(FireworkParticle(x, y, color))
    
    return firework_particles


def main():
    theme_colors = selected_theme["colors"]
    particles = [Particle(theme_colors) for _ in range(particle_count)]
    firework_particles = []
    
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BG_COLOR)
    fade_surface.set_alpha(30)
    
    time = 0
    running = True
    was_left_pressed = False
    
    explosion_wave = None
    wave_x, wave_y = 0, 0
    wave_radius = 0
    wave_active = False
    
    last_click_time = 0
    last_click_pos = (0, 0)
    double_click_threshold = 300
    double_click_distance = 30
    
    print(f"\n🎮 游戏启动！粒子数量: {particle_count}")
    print(f"🎨 颜色主题: {selected_theme['name']}")
    print("\n💡 操作说明:")
    print("   左键按住 - 吸引粒子")
    print("   右键按住 - 排斥粒子") 
    print("   中键点击 - 爆炸冲击波")
    print("   双击左键 - 烟花爆炸 🎆")
    print("   ESC - 退出\n")
    
    while running:
        mouse_buttons = pygame.mouse.get_pressed()
        was_left_pressed_now = mouse_buttons[0]
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    wave_x, wave_y = pygame.mouse.get_pos()
                    wave_radius = 0
                    wave_active = True
                elif event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    dx = click_pos[0] - last_click_pos[0]
                    dy = click_pos[1] - last_click_pos[1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    
                    if (current_time - last_click_time < double_click_threshold and 
                        distance < double_click_distance):
                        firework_particles.extend(create_firework(click_pos[0], click_pos[1], theme_colors))
                        last_click_time = 0
                    else:
                        last_click_time = current_time
                        last_click_pos = click_pos
        
        mouse_pos = pygame.mouse.get_pos()
        
        if wave_active:
            wave_radius += 12
            wave_force = max(0, 3 - wave_radius / 150)
            explosion_wave = (wave_x, wave_y, wave_radius, wave_force)
            
            if wave_radius > 500:
                wave_active = False
                explosion_wave = None
        else:
            explosion_wave = None
        
        screen.blit(fade_surface, (0, 0))
        
        for particle in particles:
            particle.update(mouse_pos, mouse_buttons, time, was_left_pressed, explosion_wave)
        
        for fp in firework_particles[:]:
            fp.update()
            if fp.life <= 0:
                firework_particles.remove(fp)
        
        if particle_count <= 120:
            draw_connections(screen, particles)
        
        for particle in particles:
            particle.draw(screen)
        
        for fp in firework_particles:
            fp.draw(screen)
        
        if wave_active:
            draw_explosion_wave(screen, wave_x, wave_y, wave_radius, theme_colors)
        
        if mouse_buttons[0]:
            cursor_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
            for r in range(50, 0, -3):
                alpha = int((50 - r) / 50 * 25)
                pygame.draw.circle(cursor_surface, (100, 150, 255, alpha), (75, 75), r)
            screen.blit(cursor_surface, (mouse_pos[0] - 75, mouse_pos[1] - 75), special_flags=pygame.BLEND_RGBA_ADD)
        elif mouse_buttons[2]:
            cursor_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
            for r in range(50, 0, -3):
                alpha = int((50 - r) / 50 * 25)
                pygame.draw.circle(cursor_surface, (255, 100, 100, alpha), (75, 75), r)
            screen.blit(cursor_surface, (mouse_pos[0] - 75, mouse_pos[1] - 75), special_flags=pygame.BLEND_RGBA_ADD)
        
        was_left_pressed = was_left_pressed_now
        
        pygame.display.flip()
        clock.tick(60)
        time += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()