import tkinter as tk
from tkinter import Tk, ttk, font, messagebox, Menu
from tkinter.ttk import Progressbar
from tkinter import DoubleVar, StringVar, IntVar, BooleanVar, Toplevel
from win32api import GetMonitorInfo, MonitorFromPoint
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from astropy.coordinates import get_body_barycentric, get_body
from astropy.time import Time
import astropy.units as u
import numpy as np
import pathlib
import os
import re
def about():
       msg1='Creator: Ross Waters'
       msg2='\nEmail: RossWatersjr@gmail.com'
       msg3='\nRevision: 2.7'
       msg4='\nLast Revision Date: 04/24/2024'
       msg5='\nMatplotlib Version 3.8.3'
       msg6='\nAstropy Version 6.0.1'
       msg7='\nProgramming Language: Python 3.12.2 64-Bit'
       msg8='\nCreated For Windows 11'
       msg=msg1+msg2+msg3+msg4+msg5+msg6+msg7+msg8
       messagebox.showinfo('About Inner Solar System 3D', msg)
def reset_axes():# Reset the axes properties
    plt.cla()
    ax.set_xlim3d([-1.1,1.1])
    ax.set_xlabel('X = AU',ha='center',color='#7b7b7b',fontsize=9,weight='normal',style='italic')
    ax.set_ylim3d([-1.1,1.1])
    ax.set_ylabel('Y = AU', ha='center',color='#7b7b7b',fontsize=9, weight='normal', style='italic')
    ax.set_zlim3d([-1.1,1.1])
    ax.set_zlabel('Z = AU',ha='center',color='#7b7b7b',fontsize=9,weight='normal',style='italic')
    ax.set_box_aspect(aspect=(1,1,1))# Set Aspect Ratio = Equal
    Anim_Fig.add_axes(ax)        
    G2V.create_sun(0.15)#Draw The Sun
    stat=grid_status.get()# Keep Grid Status Same
    if stat=='off':
        ax.axis(False)
        grid_status.set('off')
        Grid_Text.set('Turn Grid ON') 
    else:
        ax.axis(True)
        grid_status.set('on')
        Grid_Text.set('Turn Grid OFF')
def anim_advance(frame):
    if frame==0:day=(Increment.get())/24
    else:day=(Increment.get()*frame)/24
    earth_days_past.set(str('Earth Days: '+str(round(day,6)))+' / Orbits: '+str(round((day/365.256),6)))
    mercury_days_past.set(str('Mercury Days: '+str(round(23.9345/1407.6*day,6)))+' / Orbits: '+str(round(day/87.969,6)))
    venus_days_past.set(str('Venus Days: '+str(round(23.9345/5832.5*day,6)))+' / Orbits: '+str(round(day/224.701,6)))
    mars_days_past.set(str('Mars Days: '+str(round(23.9345/24.6229*day,6)))+' / Orbits: '+str(round(day/686.980,6)))
    moon_orbits.set(str('Number Of Moon Orbits (Earth) = '+str(round(day/27.3217,6))))
    if Epoch[frame]==Epoch[-1]:
        stop()
        top_entries[2]['state']="normal"
        pause_btn['state']="disabled"
        stop_btn['state']="disabled"
        start_btn['state']="normal"
        Anim_Active.set(False) # Time Frame Complete
    return G2V.orbit(frame)
def anim_start(frames, speed):# Start Animation
    top_entries[2]['state']="normal"
    pause_btn['state']="normal"
    stop_btn['state']="normal"
    start_btn['state']="disabled"
    global Anim
    Anim_Active.set(True)
    Anim=animation.FuncAnimation(fig=Anim_Fig ,func=anim_advance, repeat=False, frames=frames, blit=True, interval=speed, cache_frame_data='False')
def set_defaults():
    Anim_Active.set(False)
    Anim_Paused.set(False)
    Start_Date.set('2024-01-01T00:00:00')
    Old_StartDate.set("")
    Duration.set(1.0) # Earth Duration Years
    Old_Duration.set(0.0)# Comparison For Change
    Increment.set(24.0) # Hours (Earth Rotational Resolution)
    Old_Increment.set(0.0)
    moon_orbits.set('')
    Increment_Step.set(Increment.get()/24) # Time Increments
    ax.axis(True)
    grid_status.set('on')
    top_entries[2]['state']="normal"
    pause_btn['state']="disabled"
    stop_btn['state']="disabled"
    start_btn['state']="normal"
def start():# Start Animation
    top_entries[2]['state']="normal"
    start_btn['state']="disabled"
    stop_btn['state']="normal"
    pause_btn['state']="normal"
    if Anim_Paused.get()==True:
        Anim_Paused.set(False)
        Anim.resume()
        return
    _dur=Old_Duration.get()
    _date=Old_StartDate.get()
    _inc=Old_Increment.get()
    Anim_Paused.set(False)
    Anim_Active.set(False)
    Present_Time.set("")
    header.set("")
    moon_orbits.set("")
    earth_days_past.set('')
    earth_sun.set('')
    mercury_days_past.set('')
    mercury_distance.set('')
    mercury_time.set("")
    mercury_close.set('')        
    mercury_sun.set('')
    mars_days_past.set('')
    mars_time.set("")
    mars_close.set('')        
    mars_sun.set('')
    mars_distance.set('')
    moon_distance.set('')
    moon_time.set("")
    moon_close.set('')
    venus_days_past.set('')
    venus_distance.set('')
    venus_close.set('')
    venus_time.set("")        
    venus_sun.set('')
    sun_close.set('')
    sun_time.set("")
    Old_Moon.set(1.0e24)
    Old_Mercury.set(1.0e24)
    Old_Venus.set(1.0e24)
    Old_Mars.set(1.0e24)
    Old_Sun.set(1.0e24)
    if Duration.get()!=_dur or Start_Date.get()!=_date or Increment.get()!=_inc:# Something Changed
        Old_Duration.set(Duration.get())
        Old_StartDate.set(Start_Date.get())
        Old_Increment.set(Increment.get())
        End_Time.set("")
        if Duration.get()<= 0.0: # Duration Years
            msg1='Time Duration Must Be Set To Number > 0 For Animation.\n'
            msg2='Please Enter A Time Duration.'
            messagebox.showwarning('Time Duration', msg1+msg2)
            top_entries[1].focus
            return
        if Start_Date.get()=='': # Start Date
            msg1='A Start Date Must Be Entered For Animation.\n'
            msg2='Example: 2022-01-15'
            messagebox.showwarning('Start Date', msg1+msg2)            
            top_entries[0].focus
            return
        if Increment.get()<= 0.0: # Increment Hrs 
            msg1='Time Increment Must Be Set To Number > 0 For Animation.\n'
            msg2='Please Enter A Time Increment.'
            messagebox.showwarning('Time Increment', msg1+msg2)
            top_entries[1].focus
            return
        Old_Duration.set(Duration.get())
        Old_StartDate.set(Start_Date.get())
        Old_Increment.set(Increment.get())
        Increment_Step.set(Increment.get()/24)
        Astropy_Bodies()
        Increment_Step.set(Increment.get()/24)
        try:
            Anim.resume()
            Anim.event_source.stop()
        except Exception:
            pass
        speed=Anim_Speed.get()
        total_frames=int(len(Epoch))
        End_Time.set('   Finish Date: '+str(Epoch[-1]).replace('T','  Hrs: ')[:-4])
        anim_start(total_frames, speed)
    else:# Nothing Changed
        speed=Anim_Speed.get()
        total_frames=int(len(Epoch))
        anim_start(total_frames, speed)
def on_resize(event):
    if root.state()=="normal":
        root.font["size"]=10
        present_font["size"]=12
    elif root.state()=="zoomed":    
        root.font["size"]=12
        present_font["size"]=14
def grid(event):
    plt.ion()
    stat=grid_status.get()
    if stat=='off':
        ax.axis(True)
        grid_status.set('on')
        Grid_Text.set('Turn Grid OFF') 
    else:
        ax.axis(False)
        grid_status.set('off')
        Grid_Text.set('Turn Grid ON') 
    plt.ioff()
def pause(event):
    try:
        Anim.pause()
        Anim_Paused.set(True)
    except Exception:
        pass
    top_entries[2]['state']="normal"
    start_btn['state']="normal"
    stop_btn['state']="disabled"
    pause_btn['state']="disabled"
def stop(event=None):
    try:
        Anim.event_source.stop()
        Anim_Paused.set(False)# Restart Animation
        Anim_Active.set(False)
    except Exception:
        pass
    top_entries[2]['state']="normal"
    start_btn['state']="normal"
    pause_btn['state']="disabled"
    stop_btn['state']="disabled"
def callback(event): # Entry Widgets
    try:
        Anim.event_source.stop()
    except Exception:
        pass
    start_btn['state']="disabled"
    pause_btn['state']="disabled"
    stop_btn['state']="disabled"
    Anim_Active.set(False)
    Anim_Paused.set(False)
    start()
def unit_change(event): # AU, Metric, U.S.
    selected=event.widget.get()
    Units.set(selected)
    if Anim_Active.get()==True: # Change Units And Restart
        start_btn['state']="disabled"
        pause_btn['state']="normal"
        stop_btn['state']="normal"
        Anim_Active.set(True)
        Anim_Paused.set(False)
        Anim.resume()
    else:start()
def destroy():# X Icon Or Exit Program Clicked
    try:
        Anim.event_source.stop()
    except Exception:
        pass
    try:
        Planets_Data.clear()
        Real_Moon.clear()
    except Exception:
        pass
    for widget in root.winfo_children():# Destroys Menu Bars, Frame, Canvas And Scroll Bars
        if isinstance(widget, tk.Canvas):widget.destroy()
        else:widget.destroy()
    os._exit(0)
def menu_popup(event):# display the popup menu
    if Anim_Active.get()==False:
        try:popup.tk_popup(event.x_root, event.y_root)
        finally:popup.grab_release()
def validate_dates(string): # Entry Date Widget
    regex=re.compile(r'[(0-9-)]*$') # Date Widget, Allow Integers and -
    result=regex.match(string)
    return (string == "" 
    or (string.count(string)>0# Prevent duplicates
        and result is not None
        and result.group(0) != ""))       
def on_validate_dates(P):return validate_dates(P)
def validate_double(dbl_value): # Duration, Increment Widgets
    str_value=str(dbl_value)
    regex=re.compile(r'[(0-9.)]*$') # Allowed Integers Only
    result=regex.match(str_value)
    return (str_value == "" 
    or (str_value.count(str_value)>0 # Prevent duplicates
        and result is not None
        and result.group(0) != ""))       
def on_validate_double(P):return validate_double(P)
class Bodies: # Define Planets
    def __init__(self,name,rad,cmap):
        self.name=name   
        self.radius=np.double(rad)
        self.cmap=cmap
        xyz=np.array([0.0,0.0,0.0], dtype=float)
        x,y,z=xyz[0:3]
        u=np.linspace(0,2*np.pi,100) # Create 100 Element np Array (0 - 2*pi)
        v=np.linspace(0,np.pi,100)
        x=np.double(self.radius)*np.outer(np.cos(u),np.sin(v))+np.double(x) 
        y=np.double(self.radius)*np.outer(np.sin(u),np.sin(v))+np.double(y)
        z=np.double(self.radius)*np.outer(np.ones(np.size(u)),np.cos(v))+np.double(z)
        self.plot=ax.plot_surface(x,y,z,rstride=6,cstride=6,cmap=self.cmap,linewidth=0,alpha=1)
class G2V_Solar_System:
    def __init__(self):
        self.planets=[]
        self.Planets_Data=[]
        self.Zero_Frame=0
    def add_planet(self,planet):
        self.planets.append(planet)
    def planet_properties(self,name,radius,cmap):
        self.name=name
        self.radius=radius
        name=["mercury","venus","earth","moon","mars"]
        radius=[0.0383,0.0949,0.1,0.02724,0.0532]
        self.colormap=cmap
        u=np.linspace(0,2*np.pi, 100)
        v=np.linspace(0,np.pi,100)
        self.x=np.outer(np.cos(u),np.sin(v))
        self.y=np.outer(np.sin(u),np.sin(v))
        self.z=np.outer(np.ones(np.size(u)),np.cos(v))
        top_cm=['binary_r','copper','GnBu','Pastel1','Reds']
        btm_cm=['binary','copper_r','BuGn_r','Pastel1','Reds_r']
        for i, p in enumerate(name):
            self.name.append(name[i])
            self.radius.append(radius[i])
            top=mpl.colormaps[top_cm[i]].resampled(16)
            bottom=mpl.colormaps[btm_cm[i]].resampled(16)
            newcolors=np.vstack((top(np.linspace(0,1,128)),bottom(np.linspace(0,1,128))))
            self.colormap.append(ListedColormap(newcolors))
    def create_sun(self,rad):
        N=256
        color1=np.ones((N,4))# Create Red Colormaps (Top)
        color1[:,0]=np.linspace(255/256,1,N) # R = 255
        color1[:,1]=np.linspace(100/256,1,N) # G = 232
        color1[:,2]=np.linspace(65/256,1,N)  # B = 11
        color1_cmp = ListedColormap(color1)
        color2=np.ones((N,4))# Create Red Colormaps (Bottom)
        color2[:,0]=np.linspace(255/256,1,N)
        color2[:,1]=np.linspace(100/256,1,N)
        color2[:,2]=np.linspace(65/256,1,N)
        color2_cmp = ListedColormap(color2)
        new_cmap = np.vstack((color1_cmp(np.linspace(0, 1, 128)),color2_cmp(np.linspace(1, 0, 128))))
        cmap=ListedColormap(new_cmap)#Combine Top And Bottom Colormaps
        u=np.linspace(0,2*np.pi,100)
        v=np.linspace(0,np.pi,100)
        x=np.double(rad)*np.outer(np.cos(u),np.sin(v))
        y=np.double(rad)*np.outer(np.sin(u),np.sin(v))
        z=np.double(rad)*np.outer(np.ones(np.size(u)),np.cos(v))
        self.plot=ax.plot_surface(x,y,z,rstride=6,cstride=6,cmap=cmap,linewidth=0,alpha=1)
    def finalize_moon_data(self):# Exaggerate Moons Orbit To Accomidate Size Of Earth
        global Real_Moon
        Real_Moon={}
        Real_Moon=Planets_Data[3].copy()# Save Real Moon Data For Calculations
        earth,moon,moon_exagerated,temp={},{},{},[]
        for e in range(len(Epoch)):
            earth[e]=[element for element in Planets_Data[2][e]]
            moon[e]=[element * 70 for element in Planets_Data[3][e]]
            combined=zip(earth[e],moon[e]) # Earth + Moon
            temp=[x+y for (x,y) in combined]#  Animated Moon Data = Earth + Moon Combined
            moon_exagerated[e]=[element for element in temp]
            Planets_Data[3][e]=moon_exagerated[e]# Switch Moon Data With Exagerated Data For Displayed Animation
            temp=[]
        earth,moon,moon_exagerated,temp={},{},{},[]
    def orbit(self,frame):
        try:
            if frame==0:# 0 Frame Is Sent 3 Times By Anim Function
                if self.Zero_Frame==0:
                    reset_axes()
                    self.Zero_Frame+=1
                Increment_Step.set(Increment.get()/24)
            plots=[]
            for i, p in enumerate(self.planets):
                p.plot.remove()
                p.xyz=Planets_Data[i][frame]
                x,y,z=np.double(p.radius)*self.x+np.double(p.xyz[0]),np.double(p.radius)*self.y+np.double(p.xyz[1]),np.double(p.radius)*self.z+np.double(p.xyz[2]) 
                p.plot=ax.plot_surface(x,y,z,rstride=6,cstride=6,cmap=p.cmap,linewidth=1,alpha=1)
            time_now=str(Epoch[frame]).replace('T','  Hrs: ')[:-4]
            Present_Time.set('Present Date: '+time_now)
            if p.name=="mars": # Update All Display Widgets
                earth_moon=str(round(np.sqrt((Real_Moon[frame][0])**2+(Real_Moon[frame][1])**2+(Real_Moon[frame][2])**2),18))
                new_moon=float(earth_moon)
                sun=str(round(np.sqrt((Planets_Data[2][frame][0])**2+(Planets_Data[2][frame][1])**2+
                    (Planets_Data[2][frame][2])**2),18))
                new_sun=float(sun)
                mercury=str(round(np.sqrt((Planets_Data[0][frame][0]-Planets_Data[2][frame][0])**2+
                    (Planets_Data[0][frame][1]-Planets_Data[2][frame][1])**2+(Planets_Data[0][frame][2]-
                        Planets_Data[2][frame][2])**2),18))
                new_mercury=float(mercury)
                sun_mercury=str(round(np.sqrt((Planets_Data[0][frame][0])**2+(Planets_Data[0][frame][1])**2+
                    (Planets_Data[0][frame][2])**2),18))
                venus=str(round(np.sqrt((Planets_Data[1][frame][0]-Planets_Data[2][frame][0])**2+
                    (Planets_Data[1][frame][1]-Planets_Data[2][frame][1])**2+(Planets_Data[1][frame][2]-
                        Planets_Data[2][frame][2])**2),18))
                new_venus=float(venus)
                sun_venus=str(round(np.sqrt((Planets_Data[1][frame][0])**2+(Planets_Data[1][frame][1])**2+
                    (Planets_Data[1][frame][2])**2),18))
                mars=str(round(np.sqrt((Planets_Data[4][frame][0]-Planets_Data[2][frame][0])**2+
                    (Planets_Data[4][frame][1]-Planets_Data[2][frame][1])**2+(Planets_Data[4][frame][2]-
                        Planets_Data[2][frame][2])**2),18))
                new_mars=float(mars)
                sun_mars=str(round(np.sqrt((Planets_Data[4][frame][0])**2+(Planets_Data[4][frame][1])**2+
                    (Planets_Data[4][frame][2])**2),18))
                meas=Units.get()
                if meas=='AU': # Leave As Is
                    unit=' au'
                elif meas=='U.S.': # Convert AU To Miles
                    earth_moon=str(round(float(earth_moon)*92955807.26743,18))
                    new_moon=float(earth_moon)
                    sun=str(round(float(sun)*92955807.26743,18))
                    new_sun=float(sun)
                    mercury=str(round(float(mercury)*92955807.26743,18)) 
                    new_mercury=float(mercury)
                    sun_mercury=str(round(float(sun_mercury)*92955807.26743,18)) 
                    venus=str(round(float(venus)*92955807.26743,18))
                    new_venus=float(venus)
                    sun_venus=str(round(float(sun_venus)*92955807.26743,18))
                    mars=str(round(float(mars)*92955807.26743,18)) 
                    new_mars=float(mars)
                    sun_mars=str(round(float(sun_mars)*92955807.26743,18)) 
                    unit=' mi'
                elif meas=='Metric': # Convert AU To Kilometers
                    earth_moon=str(round(float(earth_moon)*149597870.691,18)) 
                    new_moon=float(earth_moon)
                    sun=str(round(float(sun)*149597870.691,18))
                    new_sun=float(sun)
                    mercury=str(round(float(mercury)*149597870.691,18))
                    new_mercury=float(mercury)
                    sun_mercury=str(round(float(sun_mercury)*149597870.691,18)) 
                    venus=str(round(float(venus)*149597870.691,18)) 
                    new_venus=float(venus)
                    sun_venus=str(round(float(sun_venus)*149597870.691,18))
                    mars=str(round(float(mars)*149597870.691,18)) 
                    new_mars=float(mars)
                    sun_mars=str(round(float(sun_mars)*149597870.691,18)) 
                    unit=' km'
                header.set('{Nearest Distances To Earth, Date / UTC Time}')
                moon_distance.set('Distance'+chr(8853)+' To Moon: '+earth_moon+unit)
                earth_sun.set('Distance'+chr(8853)+' To Sun: '+sun+unit)
                mercury_distance.set('Distance'+chr(8853)+' To Earth: '+mercury+unit)
                mercury_sun.set('Distance'+chr(8853)+' To Sun: '+sun_mercury+unit)
                venus_distance.set('Distance'+chr(8853)+' To Earth: '+venus+unit)
                venus_sun.set('Distance'+chr(8853)+' To Sun: '+sun_venus+unit)
                mars_distance.set('Distance'+chr(8853)+' To Earth: '+mars+unit)
                mars_sun.set('Distance'+chr(8853)+' To Sun: '+sun_mars+unit)
                tol=str(round(Increment_Step.get()*24,3))+' hrs'
                if new_sun<Old_Sun.get():# Distances And Closest Distances To Earth
                    Old_Sun.set(new_sun)
                    sun_close.set('Sun = '+str(sun)+unit)
                    sun_time.set('Date: '+time_now+' '+chr(177)+' '+tol)
                if new_moon<Old_Moon.get():
                    Old_Moon.set(new_moon)
                    moon_close.set('Moon = '+str(earth_moon)+unit)
                    moon_time.set('Date: '+time_now+' '+chr(177)+' '+tol)
                if new_mercury<Old_Mercury.get():
                    Old_Mercury.set(new_mercury)
                    mercury_close.set('Mercury = '+str(mercury)+unit)
                    mercury_time.set('Date: '+time_now+' '+chr(177)+' '+tol)
                if new_venus<Old_Venus.get():
                    Old_Venus.set(new_venus)
                    venus_close.set('Venus = '+str(venus)+unit)
                    venus_time.set('Date: '+time_now+' '+chr(177)+' '+tol)
                if new_mars<Old_Mars.get():
                    Old_Mars.set(new_mars)
                    mars_close.set('Mars = '+str(mars)+unit)
                    mars_time.set('Date: '+time_now+' '+chr(177)+' '+tol)
        except Exception as e:
            print(e)
            pass
        return plots
class Astropy_Bodies():
    def __init__(self):
        global G2V
        G2V=G2V_Solar_System()
        global Planets_Data
        Planets_Data=[]
        top_entries[2]['state']="disabled"
        exit_btn['state']="disabled"
        start_btn['state']="disabled"
        pause_btn['state']="disabled"
        stop_btn['state']="disabled"
        if Start_Date.get()=='':return
        if Duration.get()<=0: return
        if Increment_Step.get()<=0:return
        if Increment.get()<=0:return
        try:
            span=(Duration.get()*366.0)/Increment_Step.get()
            Increment_Step.set(Increment.get()/24)
            global Epoch
            Epoch=Time(Start_Date.get()) + np.arange(span)*u.hour*Increment.get()
            print(len(Epoch))
        except Exception:
            msg1='Something is not correct with Entered Text.\n'
            msg2='Please check the values and try again.'
            messagebox.showwarning('Start Date', msg1+msg2)
            return
        pb=Progressbar(root, orient='horizontal', length=100, mode='determinate')
        pb.place(relx=0.2833333, rely=0.0777777, relwidth=0.4555555, relheight=0.0244444)
        txt1=tk.Label(root, text='0%', bg='#000000', fg ='#ffffff', font=root.font)
        txt1.place(relx=0.7388888, rely=0.0777777, relwidth=0.0666666, relheight=0.0244444)
        txt2=tk.Label(root, text='Please Wait! Retrieving Planetary Data For New Time Duration.', bg='#000000', fg ='#ffffff', font=root.font)
        txt2.place(relx=0.2833333, rely=0.09555555, relwidth=0.4555555, relheight=0.0244444)
        name,radius,color_map=[],[],[]
        G2V.planet_properties(name,radius,color_map)
        for p, planet in enumerate(name): # "mercury","venus","earth","moon","mars" in solar system
            G2V.add_planet(Bodies(planet, radius[p], color_map[p]))
            data={}
            for e in range(0,len(Epoch)):
                if planet=="moon":
                    coord=get_body("moon",Epoch[e], ephemeris='builtin')
                    data[e]=[np.double(coord.cartesian.xyz[0]), np.double(coord.cartesian.xyz[1]), np.double(coord.cartesian.xyz[2])]
                else:
                    coord=get_body_barycentric(planet, Epoch[e], ephemeris='builtin')
                    data[e]=[np.double(coord.xyz[0]), np.double(coord.xyz[1]), np.double(coord.xyz[2])]
                root.update_idletasks()
                pb['value']+=100/(len(Epoch)*5)
                txt1['text']=round(pb['value'],1),'%'
            Planets_Data.append(data)
        G2V.finalize_moon_data()    
        pb.destroy()
        txt1.destroy()
        txt2.destroy()
        start_btn['state']="normal"
        top_entries[2]['state']="normal"
        exit_btn['state']="normal"
if __name__ == "__main__":
    root=Tk()
    style=ttk.Style()
    style.theme_use('classic')
    style.map('TCombobox', background=[('readonly','#000000')])# Down Arrow
    style.map('TCombobox', fieldbackground=[('readonly','#000000')])
    style.map('TCombobox', selectbackground=[('readonly','#000000')])
    style.map('TCombobox', selectforeground=[('readonly', '#a7f8f8')])
    root.wm_title("3D Inner Solar System")
    dir=pathlib.Path(__file__).parent.absolute()
    filename='3DSpace.ico'
    path=os.path.join(dir, filename)
    root.iconbitmap(path)
    root.font=font.Font(family='lucidas', size=10, weight='normal', slant='italic')
    present_font=font.Font(family='lucidas', size=12, weight='normal', slant='italic')
    monitor_info=GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area=monitor_info.get("Work")
    monitor_area=monitor_info.get("Monitor")
    taskbar_height = monitor_area[3] - work_area[3]
    screen_width=work_area[2]
    screen_height=work_area[3]
    taskbar_hgt=(monitor_area[3]-work_area[3])
    root_hgt=(screen_height-taskbar_height)*0.8
    root_wid=screen_width*0.8 
    x=(screen_width/2)-(root_wid/2)
    y=(screen_height/2)-(root_hgt/2)
    root.geometry('%dx%d+%d+%d' % (root_wid, root_hgt, x, y, ))
    root.configure(bg='#000000')
    root.bind("<Configure>", on_resize)
    root.option_add('*TCombobox*Listbox.font', root.font)
    root.protocol("WM_DELETE_WINDOW", destroy)
    root.bind("<Button-3>", menu_popup)
    px=1/plt.rcParams['figure.dpi']
    dpi=root.winfo_fpixels('1i')
    Anim_Fig=plt.figure(figsize=(root_hgt*px,root_wid*px),facecolor='#000000',dpi=dpi)
    canvas=FigureCanvasTkAgg(Anim_Fig, master=root)
    ax=Anim_Fig.add_subplot(111, projection="3d")
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas = Toplevel
    ax.set_facecolor('#000000')
    ax.xaxis.pane.set_color('#000000')
    ax.xaxis.pane.fill=True
    ax.yaxis.pane.set_color('#000000')
    ax.yaxis.pane.fill=True
    ax.zaxis.pane.set_color('#000000')
    ax.zaxis.pane.fill=True
    ax.tick_params(axis='x',colors='#7b7b7b')
    ax.tick_params(axis='y',colors='#7b7b7b')
    ax.tick_params(axis='z',colors='#7b7b7b')
    ax.xaxis._axinfo["grid"].update({"linewidth":0.5})
    ax.yaxis._axinfo["grid"].update({"linewidth":0.5})
    ax.zaxis._axinfo["grid"].update({"linewidth":0.5})
    ax.xaxis._axinfo["grid"].update({"color":('#7b7b7b')})
    ax.yaxis._axinfo["grid"].update({"color":('#7b7b7b')})
    ax.zaxis._axinfo["grid"].update({"color":('#7b7b7b')})
    ax.view_init(azim=-45, elev=25)
    plt.tight_layout()
    Anim_Active=BooleanVar()
    Anim_Speed=IntVar()
    Anim_Paused=BooleanVar()
    Old_Sun=DoubleVar()
    Old_Moon=DoubleVar()
    Old_Mercury=DoubleVar()
    Old_Venus=DoubleVar()
    Old_Mars=DoubleVar()
    Present_Time=StringVar() # Present Date Label
    End_Time=StringVar()
    earth_days_past=StringVar()
    moon_distance=StringVar()
    moon_orbits=StringVar()
    earth_sun=StringVar()
    mercury_days_past=StringVar()
    mercury_distance=StringVar()
    mercury_sun=StringVar()
    venus_days_past=StringVar()
    venus_distance=StringVar()
    venus_sun=StringVar()
    mars_days_past=StringVar()
    mars_distance=StringVar()
    mars_sun=StringVar()
    header=StringVar()
    sun_close=StringVar()
    sun_time=StringVar()
    moon_close=StringVar()
    moon_time=StringVar()
    mercury_close=StringVar()
    mercury_time=StringVar()
    venus_close=StringVar()
    venus_time=StringVar()
    mars_close=StringVar()
    mars_time=StringVar()
    Start_Date=StringVar()
    Old_StartDate=StringVar()
    Duration=DoubleVar()
    Old_Duration=DoubleVar()
    Increment=DoubleVar()
    Old_Increment=DoubleVar()
    Increment_Step=DoubleVar()
    grid_status=StringVar()
    Grid_Text=StringVar()
    top_lbls=[]
    x_rel=[0.095,0.215,0.325,0.44]
    wid=[0.11,0.1,0.105,0.05]
    txt=['Start Date / UTC Time','Earth Duration (Yrs.)','Time Increment (Hrs.)','Units']
    for index, element in enumerate(x_rel): # Labels For Top Row Entries
        top_lbls.append([index])
        top_lbls[index]=tk.Label(root, bg='#000000', fg='#ffffff', font=root.font, 
            text=txt[index], justify='left', anchor='c')
        top_lbls[index].place(relx=element, rely=0.005, relwidth=wid[index], relheight=0.0344)
    top_entries=[]
    validates=[validate_dates,validate_double,validate_double]
    cmds=[on_validate_dates,on_validate_double,on_validate_double]
    txt_var=[Start_Date,Duration,Increment]
    for index, element in enumerate(txt_var): # Top Row Entries
        top_entries.append([index])
        top_entries[index]=tk.Entry(root, bg='#000000', fg='#a7f8f8', textvariable=element, font=root.font, 
                justify='center',insertbackground='#ffffff')
        top_entries[index].place(relx=x_rel[index], rely=0.0366666, relwidth=wid[index], relheight=0.0344)
        top_entries[index]['validatecommand']=(top_entries[index].register(validates[index]),'%P','%d')
        cmd=(top_entries[index].register(cmds[index]), '%P')
        top_entries[index].config(validate="key", validatecommand=cmd)
        top_entries[index].config(cursor="xterm #ffffff")
        top_entries[index].bind("<Button-1>", pause)
        top_entries[index].bind('<Return>', callback)
    start_btn=tk.Button(root, text='Start', background="#000000", foreground='#ffffff', font=root.font, command=lambda: start())
    start_btn.place(relx=0.50, rely=0.0366666, relwidth=0.05, relheight=0.0344)
    pause_btn=tk.Button(root, text='Pause', background="#000000", foreground='#ffffff', font=root.font)
    pause_btn.place(relx=0.56, rely=0.0366666, relwidth=0.05, relheight=0.0344)
    pause_btn.bind("<Button-1>", pause)
    stop_btn=tk.Button(root, text='Stop', background="#000000", foreground='#ffffff', font=root.font)
    stop_btn.place(relx=0.62, rely=0.0366666, relwidth=0.05, relheight=0.0344)
    stop_btn.bind("<Button-1>", stop)
    Units=tk.StringVar()
    units_cb=ttk.Combobox(root, textvariable=Units, background="#000000", foreground='#a7f8f8', font=root.font, justify='center')
    units_cb.place(relx=0.44, rely=0.0366666, relwidth=0.05, relheight=0.0344) # using place method
    units_cb['values']=('AU','U.S.','Metric')
    units_cb['state']='readonly'
    units_cb.current(0)
    units_cb.bind("<Button-1>", pause)
    units_cb.bind('<<ComboboxSelected>>', unit_change)
    Grid_Text.set('Turn Grid OFF') 
    grid_btn=tk.Button(root, textvariable=Grid_Text, background="#000000", foreground='#ffffff', font=root.font,)
    grid_btn.place(relx=0.68, rely=0.0366666, relwidth=0.08, relheight=0.0344)
    grid_btn.bind("<Button-1>", grid)
    exit_btn=tk.Button(root, text='Exit Program', background="#000000", foreground = '#ffffff', font=root.font, command=lambda: destroy())
    exit_btn.place(relx=0.77, rely=0.0366666, relwidth=0.08, relheight=0.0344)
    present_lbl=tk.Label(root, bg='#000000', fg='#a7f8f8', font=present_font, 
        text='', textvariable=Present_Time, anchor='w')
    present_lbl.place(relx=0.02, rely=0.15, relwidth=0.22, relheight=0.03)
    end_lbl=tk.Label(root, bg='#000000', fg='#a7f8f8', font=present_font, 
        text='', textvariable=End_Time, anchor='w')
    end_lbl.place(relx=0.02, rely=0.18, relwidth=0.22, relheight=0.03)
    strvar=[earth_days_past,moon_distance,moon_orbits,earth_sun,mercury_days_past,mercury_distance,
        mercury_sun,venus_days_past,venus_distance,venus_sun,mars_days_past,mars_distance,mars_sun]
    color=['#3292ea','#3292ea','#3292ea','#3292ea','#d2d2d2','#d2d2d2','#d2d2d2','#cd9f6d','#cd9f6d',
        '#cd9f6d','#cc0000','#cc0000','#cc0000']
    do_lbl=[] # Days Past Data / Orbits Data
    y=0.23 
    for index, element in enumerate(strvar):
        do_lbl.append([index])
        do_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text='', textvariable=element, justify='left', anchor='w')
        do_lbl[index].place(relx=0.02, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    y+=0.025
    nd_lbl=[] # Nearest Distance / Date/Time Data
    strvar=[header,sun_close,sun_time,moon_close,moon_time,mercury_close,mercury_time,venus_close,venus_time,mars_close,mars_time]
    color=['#a7f8f8','#ff7469','#ff7469','#ffffff','#ffffff','#999999','#999999','#cd9f6d',
        '#cd9f6d','#cc0000','#cc0000']
    for index, element in enumerate(strvar):
        nd_lbl.append([index])
        nd_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        textvariable=element, justify='left', anchor='w')
        nd_lbl[index].place(relx=0.02, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    y=0.11
    bd_lbl=[] # Body Diameters
    text=['{Body Diameters}','Sun = 1,391,983 km, 864,938 mi','Earth = 12,741.98 km, 7,917.5 mi',
        'Moon = 3,474.735 km, 2,159.1 mi','Mercury = 4,879.37 km, 3,031.9 mi',
        'Venus = 12,103.554 km, 7,520.8 mi','Mars = 6,779.04 km, 4,213.3 mi']
    color=['#a7f8f8','#ff7469','#3292ea','#f3f6f4','#999999','#cd9f6d','#cc0000']
    for index, element in enumerate(text):
        bd_lbl.append([index])
        bd_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text=element, justify='left', anchor='w')
        bd_lbl[index].place(relx=0.8, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    bm_lbl=[] # Body Mass
    text=['{Body Masses}','Sun = 1.98847 x 10'+ chr(179) + chr(8304) + ' kg','Earth = 5.97219 x 10'+ chr(178) + chr(8308) + ' kg',
        'Moon = 7.34767 x 10'+ chr(178) + chr(178) + ' kg','Mercury = 3.30104 x 10'+ chr(178) + chr(179) + ' kg',
        'Venus = 4.86732 x 10'+ chr(178) + chr(8308) + ' kg','Mars = 6.4169 x 10'+ chr(178) + chr(179) + ' kg']
    for index, element in enumerate(text):
        bm_lbl.append([index])
        bm_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text=element, justify='left', anchor='w')
        bm_lbl[index].place(relx=0.8, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    rp_lbl=[] # Rotation Periods
    color=['#a7f8f8','#3292ea','#f3f6f4','#999999','#cd9f6d','#cc0000']
    text=['{Rotational Periods}','Earth = 23.9345 hrs.','Moon = 655.7 hrs.',
        'Mercury = 1407.6 hrs.','Venus = -5832.5 hrs.','Mars = 24.6229 hrs.']
    for index, element in enumerate(text):
        rp_lbl.append([index])
        rp_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text=element, justify='left', anchor='w')
        rp_lbl[index].place(relx=0.8, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    op_lbl=[] # Orbital Periods
    text=['{Orbital Periods}','Earth = 365.256 days','Moon (Earth) = 27.3217 days',
        'Mercury = 87.969 days','Venus = 224.701 days','Mars = 686.980 days']
    for index, element in enumerate(text):
        op_lbl.append([index])
        op_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text=element, justify='left', anchor='w')
        op_lbl[index].place(relx=0.8, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    ov_lbl=[] # Orbital Velocities
    text=['{Orbital Velocities}','Earth = 29.8 km/sec, 18.5 mi/sec','Moon = 1.022 km/sec, 0.6350 mi/sec ',
        'Mercury = 47.4 km/sec, 29.4 mi/sec','Venus = 35.0 km/sec, 21.8 mi/sec','Mars = 21.4 km/sec, 15.0 mi/sec']
    for index, element in enumerate(text):
        ov_lbl.append([index])
        ov_lbl[index]=tk.Label(root, bg='#000000', fg=color[index], font=root.font, 
        text=element, justify='left', anchor='w')
        ov_lbl[index].place(relx=0.8, rely=y, relwidth=0.235, relheight=0.03)
        y+=0.025
    strvar.clear()
    color.clear()
    text.clear()    
    popup=Menu(root, tearoff=0) # PopUp Menu
    popup.add_command(label="About", background='aqua', command=lambda:about())
    set_defaults()
root.mainloop()