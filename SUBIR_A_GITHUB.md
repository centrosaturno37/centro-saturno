# Instrucciones para subir a GitHub Pages

## Paso 1 – Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre del repo: `centro-saturno`
3. Ponlo como **Public**
4. NO inicialices con README
5. Clic en "Create repository"

## Paso 2 – Subir desde tu PC (abre PowerShell o Terminal)
```
cd "C:\Users\mc456\OneDrive\Desktop\mis proyectos\centro-saturno-web"
git remote add origin https://github.com/centrosaturno37/centro-saturno.git
git branch -M main
git push -u origin main
```
(Reemplaza TU_USUARIO con tu nombre de usuario de GitHub)

## Paso 3 – Activar GitHub Pages
1. Ve a tu repo en GitHub
2. Settings → Pages
3. Source: **Deploy from a branch**
4. Branch: **main**, folder: **/ (root)**
5. Clic en Save

## Tu link público será:
https://centrosaturno37.github.io/centro-saturno/

Este link funciona en Android, iPhone, WhatsApp, Facebook y cualquier navegador.

## Para el futuro – Play Store
Usa Capacitor o Cordova para convertirlo en APK:
```
npm install -g @capacitor/cli
npx cap init "Centro Saturno" "com.centrosaturno.app"
npx cap add android
npx cap copy
npx cap open android
```
