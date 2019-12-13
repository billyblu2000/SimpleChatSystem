from snake import *
import pygame
import sys
import random

class Game:
    
    SCREEN_X = 600
    SCREEN_Y = 600

    def show_text(self,screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):   
        #获取系统字体，并设置文字大小  
        cur_font = pygame.font.SysFont("宋体", font_size)  
        #设置是否加粗属性  
        cur_font.set_bold(font_bold)  
        #设置是否斜体属性  
        cur_font.set_italic(font_italic)  
        #设置文字内容  
        text_fmt = cur_font.render(text, 1, color)  
        #绘制文字  
        screen.blit(text_fmt, pos)


    def run(self):
        pygame.init()
        screen_size = (SCREEN_X,SCREEN_Y)
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Snake')
        clock = pygame.time.Clock()
        scores = 0
        isdead = False

        # 蛇/食物
        snake = Snake()
        food = Food()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    snake.changedirection(event.key)
                    # 死后按space重新
                    if event.key == pygame.K_SPACE and isdead:
                        return main()


            screen.fill((255,255,255))

            # 画蛇身 / 每一步+1分
            if not isdead:
                scores+=1
                snake.move()
            for rect in snake.body:
                pygame.draw.rect(screen,(20,220,39),rect,0)

            # 显示死亡文字
            isdead = snake.isdead()
            if isdead:
                self.show_text(screen,(100,200),'YOU DEAD!',(227,29,18),False,100)
                self.show_text(screen,(150,260),'press space to try again...',(0,0,22),False,30)

            # 食物处理 / 吃到+50分
            # 当食物rect与蛇头重合,吃掉 -> Snake增加一个Node
            if food.rect == snake.body[0]:
                scores+=50
                food.remove()
                snake.addnode()

            # 食物投递
            food.set()
            pygame.draw.rect(screen,(136,0,21),food.rect,0)

            # 显示分数文字
            self.show_text(screen,(50,500),'Scores: '+str(scores),(223,223,223))

            pygame.display.update()
            clock.tick(10)
            
if __name__ == "__main__":
    
    game = Game()
    game.run()
    
