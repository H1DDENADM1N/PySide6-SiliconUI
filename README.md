
<p align="center">  
  
  <a href="#">
    <img src="assets/readme/silicon_main.png" alt="Logo"  >
  </a>
  
  <h2 align="center">PySide6-SiliconUI</h2>
  <p align="center">A powerful and artistic UI library based on PySide6</p>

<p align="center">
    English | <a href="docs/README_zh.md">简体中文</a>
</p>

## Install
I'm using [pdm](https://github.com/pdm-project/pdm) as Python package and dependency manager.

```powershell
pdm install
```

> ⚠️ This project is still under active development. It is **not yet available on PyPi**, but will be in the future.


## Run Examples
To quick start, run:
```powershell
.\.venv\Scripts\activate.ps1
python ".\examples\Gallery for siui\start.py"
```

### Refactoring Plan

The refactoring of widgets is nearing completion. You can try them on the "Refactored Widgets" page in the Gallery.

**Please note**:  
If you plan to start a project using PyQt-SiliconUI in the near future, it is **highly recommended to use only the widgets listed under “Refactored Widgets”**. 
The older widgets have many issues and are being gradually replaced.  

Similarly, the application templates are also under a complete overhaul. Work on them will begin once the core widget and component refactors are done. 
Since the current templates contain many flaws and have poor implementations, 
**we strongly advise against using the old application templates for real-world projects until the refactor is complete**.

### Refactored Modules Overview

Below are actively maintained modules. Once these are fully implemented, outdated ones will be removed from the repository.

#### Widgets

- `siui/components/button.py` – Refactored button widgets  
- `siui/components/container.py` – Refactored containers managed using Qt’s layout system  
- `siui/components/editor.py` – Refactored input/edit widgets  
- `siui/components/graphic.py` – Proxy widgets, wrappers, and graphic-related utilities  
- `siui/components/label.py` – Widgets for displaying text and images, plus uncategorized ones  
- `siui/components/layout.py` – New implementations of flow and waterfall layouts, also using Qt layouts  
- `siui/components/menu_.py` – Menu components  
- `siui/components/popover.py` – Popover-style widgets such as date pickers and time pickers  
- `siui/components/progress_bar_.py` – Refactored progress bar widgets  
- `siui/components/slider_.py` – Refactored sliders, including horizontal sliders and scrollbar handles  

#### Core Features

- `siui/core/animation.py` – Refactored animation utilities  
- `siui/core/event_filter.py` – Various event filters  
- `siui/core/painter.py` – Core drawing-related functions  


## License
PySide6-SiliconUI is licensed under [GPLv3](LICENSE) 

Copyright © 2024-2025 by H1DDENADM1N.
