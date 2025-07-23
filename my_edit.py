#!/bin/python3
import curses
from curses import wrapper
from curses.textpad import Textbox , rectangle
import sys
import signal

def head_init(stdscr,maxX):
  head=curses.newwin(1,maxX,0,0)
  head.bkgd(' ', curses.A_REVERSE)
  head.addstr(0,maxX//2-7,'Kast Editor')
  head.refresh()
  return head


def foot_display(foot,maxX):
 foot.addstr(1,maxX//2-4,'^X',curses.A_REVERSE)
 foot.addstr(' Exit')
 foot.refresh()



def to_exit(stdscr,text_window,foot,buffer,filename):
 foot.clear()
 maxY,maxX = stdscr.getmaxyx()
 foot.addstr(1,0,' Y',curses.A_REVERSE)
 foot.addstr(' YES')
 foot.addstr(2,0,' N',curses.A_REVERSE)
 foot.addstr(' NO')
 foot.addstr(1,maxX//2,' C',curses.A_REVERSE)
 foot.addstr(' Cancel')
 foot.addstr(0,0,'Do you want to save this buffer ? ' )
 foot.refresh()
 while True :
  a=chr(stdscr.getch())
  if (a=='N' or a=='n' ):
   exit()
  elif(a =='C' or a=='c' ):
    y,x= text_window.getyx()
    foot.clear()
    foot_display(foot,maxX)
    text_window.move(y,x)
    break 
  elif(a=='y' or a=='Y'):
    if (filename==''):
     curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
     curses.echo()
     stdscr.clear()
     stdscr.refresh()
     
     height = 7
     width = maxX - 4
     start_y = maxY // 2 - height // 2
     start_x = 2
     win = curses.newwin(height, width, start_y, start_x)
     win.box()
     
     rect_top = 1
     rect_left = 2
     rect_bottom = height - 2
     rect_right = width - 3
     rectangle(win, rect_top, rect_left, rect_bottom, rect_right)
     prompt = "Enter the file name: "
     prompt_y = rect_top + 2
     prompt_x = maxX // 4
     if prompt_x + len(prompt) + 20 > rect_right:
       prompt_x = rect_right - len(prompt) - 20

     win.addstr(prompt_y, prompt_x, prompt)
     win.attron(curses.color_pair(1))
     win.refresh()
     filename = win.getstr(24).decode() 
     if (filename==''):
      filename='buffer.txt'
      
    f=open(filename,'w')
    f.write(buffer)
    f.close()
    exit()




def main(stdscr):
 signal.signal(signal.SIGINT,signal.SIG_IGN)
 stdscr.clear()
 stdscr.refresh()

 maxY,maxX = stdscr.getmaxyx()

 head=head_init(stdscr,maxX)

 foot=curses.newwin(3,maxX,maxY-3,0)
 foot_display(foot,maxX)

 text_window=curses.newpad(1000,300) # lines , cols
 if (len(sys.argv) ==2):
  filename=sys.argv[1]
  try :
   f=open(sys.argv[1],'r')
   lines=f.readlines()
   if (lines==[]):
    lines= ['']
   f.close()
  except:
    filename=sys.argv[1]
    lines=['']
 else:
  filename=''
  lines=['']

 buffer = ''.join(lines)
 text_window.addstr(0,0,buffer)
 text_window.clear()
 text_window.refresh(0,0,1,0,maxY-4,maxX-1)
 y,x =text_window.getyx()

 while True :
   text_window.clear()
   text_window.addstr(0,0,buffer)
   text_window.move(y,x)
   if (x >maxX-1):
    text_window.refresh(y -maxY +5 if y - maxY +5 > 0 else 0 ,maxX,1,0,maxY-4,maxX-1)
   else:
    text_window.refresh( y -maxY +5 if y - maxY +5 > 0 else 0 ,0,1,0,maxY-4,maxX-1)
   a=stdscr.getch()

   if (a==curses.KEY_UP):
    if (y>0):
     y -=1
     line =lines[y]
     x = min(x, len(line.rstrip('\n')))

   elif (a==curses.KEY_DOWN):
    if (y +1< len(lines)) :
     y=y+1
     line=lines[y]
     x = min(x, len(line.rstrip('\n')))
   elif (a == curses.KEY_LEFT):
    if (x>0):
     x=x-1
    else:
     if y!=0 :
      line=lines[y-1]
      y -= 1
      line = lines[y]
      x = len(line.rstrip('\n'))
      

   elif (a == curses.KEY_RIGHT):
        line = lines[y]
        line_limit = len(line.rstrip('\n'))
        if x < line_limit :
            x += 1
        elif y + 1 < len(lines):
            y += 1
            x = 0

   elif (a  in (curses.KEY_BACKSPACE, 127, 8)):
    if x==0 :
     if y==0 :
       pass
     else :
      next=lines.pop(y)
      prev=lines[y-1]
      x=len(prev)-1
      lines[y-1]=prev[:-1]+next
      y=y-1
    else:
      curr=lines[y]
      lines[y]=curr[:x-1]+curr[x:]
      x=x-1 

   elif a in (10,13, curses.KEY_ENTER):
    nw_line=lines[y]
    lines[y]=nw_line[:x]+'\n'
    nw_line=nw_line[x:]
    y , x = (y+1 , 0) 
    lines.insert(y ,nw_line)
    nw_line=nw_line[x:]
   
   elif a == 24 :
     to_exit(stdscr,text_window,foot,buffer,filename)
  
   elif a <=126 and a >=32 :
     if (y < len(lines)):
      line=lines[y]
      line=line[:x]+chr(a)+line[x:]
      x=x+1
      lines[y]=line
     else:
      pass
   buffer = ''.join(lines)


 stdscr.getch()

wrapper(main)
