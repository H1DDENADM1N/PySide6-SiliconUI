from __future__ import annotations

import sys
from dataclasses import dataclass, field

from PySide6.QtCore import Property, QRectF, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPainterPath
from PySide6.QtWidgets import QLineEdit
from pathlib import Path

sys.path.append(str(Path().cwd()))

from siui.core import createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont
from siui.siui_typing import T_WidgetParent


@dataclass
class LineEditStyleData:
    STYLE_TYPES = ["Slider"]
    title_background_color: QColor = field(default_factory=lambda: QColor("#28252d"))
    title_color_idle: QColor = field(default_factory=lambda: QColor("#918497"))
    title_color_focused: QColor = field(default_factory=lambda: QColor("#D1CBD4"))
    title_color_error: QColor = field(default_factory=lambda: QColor("#b27b84"))

    text_background_color: QColor = field(default_factory=lambda: QColor("#201d23"))
    text_color: QColor = field(default_factory=lambda: QColor("#D1CBD4"))

    text_indicator_color_idle: QColor = field(default_factory=lambda: QColor("#00A681BF"))
    text_indicator_color_editing: QColor = field(default_factory=lambda: QColor("#A681BF"))
    text_indicator_color_error: QColor = field(default_factory=lambda: QColor("#d36764"))


class SiLineEdit(QLineEdit):
    class SiLineEditProperty:
        TitleColor = "titleColor"
        TextIndicatorColor = "textIndicatorColor"
        TextIndicatorWidth = "textIndicatorWidth"

    def __init__(self, parent: T_WidgetParent = None, title: str = "Untitled Edit Box") -> None:
        super().__init__(parent)

        self.style_data = LineEditStyleData()
        self._title_font = SiFont.getFont(size=13)
        self._title = title
        self._title_width = 160
        self._title_color = self.style_data.title_color_idle
        self._text_indi_color = self.style_data.text_indicator_color_idle
        self._text_indi_width = 0
        self._text_bg_width_progress = 0

        self.title_color_ani = SiExpAnimationRefactor(self, self.SiLineEditProperty.TitleColor)
        self.title_color_ani.init(1 / 6, 0.001, self._title_color, self._title_color)

        self.text_indicator_color_ani = SiExpAnimationRefactor(self, self.SiLineEditProperty.TextIndicatorColor)
        self.text_indicator_color_ani.init(1 / 4, 0.01, self._text_indi_color, self._text_indi_color)

        self.text_indicator_width_ani = SiExpAnimationRefactor(self, self.SiLineEditProperty.TextIndicatorWidth)
        self.text_indicator_color_ani.init(1 / 8, 0.01, 0, 0)

        self.setFont(SiFont.getFont(size=14))
        self._initStyleSheet()

        self.textChanged.connect(self._onTextEdited)
        self.returnPressed.connect(self._onReturnPressed)

    def _initStyleSheet(self) -> None:
        self.setStyleSheet(
            "QLineEdit {"
            "     selection-background-color: #493F4E;"
            "     background-color: transparent;"
            f"    color: {self.style_data.text_color.name()};"
            "     border: 0px;"
            f"    padding-left: {self._title_width + 18}px;"
            "     padding-right: 18px;"
            "     padding-bottom: 1px;"
            "}"
        )

    @Property(QColor)
    def titleColor(self):
        return self._title_color

    @titleColor.setter
    def titleColor(self, value: QColor):
        self._title_color = value
        self.update()

    @Property(float)
    def textBackgroundWidthProgress(self):
        return self._text_bg_width_progress

    @textBackgroundWidthProgress.setter
    def textBackgroundWidthProgress(self, value: float):
        self._text_bg_width_progress = value
        self.update()

    @Property(QColor)
    def textIndicatorColor(self):
        return self._text_indi_color

    @textIndicatorColor.setter
    def textIndicatorColor(self, value: QColor):
        self._text_indi_color = value
        self.update()

    @Property(float)
    def textIndicatorWidth(self):
        return self._text_indi_width

    @textIndicatorWidth.setter
    def textIndicatorWidth(self, value: float):
        self._text_indi_width = value
        self.update()

    def title(self) -> str:
        return self._title

    def setTitle(self, title: str) -> None:
        self._title = title
        self.update()

    def titleWidth(self) -> int:
        return self._title_width

    def setTitleWidth(self, width: int) -> None:
        self._title_width = width
        self._initStyleSheet()
        self.update()

    def notifyInvalidInput(self):
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_error)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_error)
        self.title_color_ani.start()
        self.text_indicator_width_ani.setEndValue(self.width() - self._title_width - 36)
        self.text_indicator_width_ani.start()

    def _onTextEdited(self, text: str):
        metric = QFontMetrics(self.font())
        text_rect = QRectF(self._title_width, 0, self.width() - self._title_width, self.height())
        width = min(metric.boundingRect(text).width(), text_rect.width() - 36)

        self.text_indicator_width_ani.setEndValue(width)
        self.text_indicator_width_ani.start()

    def _onReturnPressed(self):
        # find the nearest edit box and give focus to it.
        target = None
        for widget in self.parent().findChildren(QLineEdit):
            if widget.x() > self.x() or widget.y() > self.y():
                if target is None:
                    target = widget
                    continue
                if widget.x() < target.x() or widget.y() < target.y():
                    target = widget
                    continue

        if target is not None:
            target.setFocus()
        self.clearFocus()

    def _drawTitleBackgroundPath(self, rect: QRectF) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        return path

    def _drawTitleRect(self, painter: QPainter, rect: QRectF) -> None:
        sd = self.style_data
        text_rect = QRectF(rect.x() + 17, rect.y(), rect.width(), rect.height() - 1)

        painter.setBrush(sd.title_background_color)
        painter.drawPath(self._drawTitleBackgroundPath(rect))

        painter.setPen(self._title_color)
        painter.setFont(self._title_font)
        painter.drawText(painter.boundingRect(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self._title), self._title)

        painter.setPen(Qt.NoPen)

    def _drawTextBackgroundPath(self, rect: QRectF) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        return path

    def _drawTextIndicatorPath(self, rect: QRectF) -> QPainterPath:
        indi_rect = QRectF(rect.x() + 16, rect.y() + 34, self._text_indi_width + 8, 2)
        path = QPainterPath()
        path.addRoundedRect(indi_rect, 1, 1)
        return path

    def _drawTextRect(self, painter: QPainter, rect: QRectF) -> None:
        sd = self.style_data
        painter.setBrush(sd.text_background_color)
        painter.drawPath(self._drawTextBackgroundPath(rect))

        painter.setBrush(self._text_indi_color)
        painter.drawPath(self._drawTextIndicatorPath(rect))

    def paintEvent(self, a0):
        title_rect = QRectF(0, 0, self.width(), self.height())
        text_rect = QRectF(self._title_width, 0, self.width() - self._title_width, self.height())

        renderHints = (
            QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawTitleRect(painter, title_rect)
            self._drawTextRect(painter, text_rect)

        super().paintEvent(a0)

    def focusInEvent(self, a0):
        super().focusInEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_editing)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_focused)
        self.title_color_ani.start()

        self._onTextEdited(self.text())

    def focusOutEvent(self, a0):
        super().focusOutEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_idle)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_idle)
        self.title_color_ani.start()

        self._onTextEdited("")
