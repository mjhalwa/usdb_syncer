"""Controller for the filter tree."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import QModelIndex, Qt

from usdb_syncer import db
from usdb_syncer.gui.utils import keyboard_modifiers

from .item import Filter, FilterItem, RootItem, VariantItem
from .model import TreeModel, TreeProxyModel

if TYPE_CHECKING:
    from usdb_syncer.gui.mw import MainWindow


class FilterTree:
    """Controller for the filter tree."""

    def __init__(self, mw: MainWindow) -> None:
        self.mw = mw
        self.view = mw.search_view
        self._build_tree()
        self._model = TreeModel(mw, self.root)
        self._proxy_model = TreeProxyModel(self.view, self._model)
        self.view.setHeaderHidden(True)
        self.view.setModel(self._proxy_model)
        self.view.clicked.connect(self._on_click)
        # mw.line_edit_search_filters.textChanged.connect(self._proxy_model.set_filter)

    def _build_tree(self) -> None:
        self.root = RootItem()
        for filt in Filter:
            item = FilterItem(data=filt, parent=self.root)
            self.root.add_child(item)
            item.set_children(
                VariantItem(data=variant, parent=item) for variant in filt.variants()
            )

    def _on_click(self, index: QModelIndex) -> None:
        item = self._model.item_for_index(self._proxy_model.mapToSource(index))
        for changed in item.toggle_checked(keyboard_modifiers().ctrl):
            idx = self._model.index_for_item(changed)
            self._model.dataChanged.emit(idx, idx, [Qt.ItemDataRole.CheckStateRole])

    def connect_filter_changed(self, func: Callable[[], None]) -> None:
        self._model.dataChanged.connect(func)

    def build_search(self, search: db.SearchBuilder) -> None:
        for filt in self.root.children:
            filt.build_search(search)
