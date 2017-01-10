from ui_functions.treeViewClasses import *


def update_ow_menu_buttons(ui):
    if ui.selected_table is None:
        ui.addOwButton.setEnabled(False)
        ui.insertOwButton.setEnabled(False)
        ui.resizeOwButton.setEnabled(False)
        ui.removeOwButton.setEnabled(False)

    if ui.selected_ow is None and ui.selected_table is not None:
        # A Table was selected
        ui.addOwButton.setEnabled(True)
        ui.insertOwButton.setEnabled(True)
        ui.resizeOwButton.setEnabled(False)
        ui.removeOwButton.setEnabled(False)
        return

    if ui.selected_ow is not None and ui.selected_table is not None:
        # An OW was selected
        ui.addOwButton.setEnabled(True)
        ui.insertOwButton.setEnabled(True)
        ui.resizeOwButton.setEnabled(True)
        ui.removeOwButton.setEnabled(True)
        return


def update_ow_text_menu(ui):
    if ui.selected_ow is None and ui.selected_table is not None:
        # Table selected
        ui.typeLabel.setText("")
        ui.framesLabel.setText("")
        ui.pointerAddressLabel.setText("")
        ui.dataAddressLabel.setText("")
        ui.framesPointersLabel.setText("")
        ui.framesAddressLabel.setText("")

    if ui.selected_ow is not None and ui.selected_table is not None:
        # OW selected
        ow_type = root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].frames.get_type()
        width, height = get_frame_dimensions(ow_type)

        ui.typeLabel.setText(str(ow_type) + "  [" + str(width) + 'x' + str(height) + ']')
        ui.framesLabel.setText(str(ui.OWTreeView.selectionModel().currentIndex().internalPointer().frames))
        ui.pointerAddressLabel.setText(capitalized_hex(
            root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].ow_pointer_address))
        ui.dataAddressLabel.setText(capitalized_hex(
            root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].ow_data_address))
        ui.framesPointersLabel.setText(capitalized_hex(
            root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].frames.frames_pointers_address))
        ui.framesAddressLabel.setText(capitalized_hex(
            root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].frames.frames_address))


def update_tables_menu_buttons(ui):
    # They are actually always open
    ui.removeTableButton.setEnabled(False)

    if ui.selected_table is None:
        ui.removeTableButton.setEnabled(False)
    else:
        if ui.tree_model.tablesCount() != 1 or root.get_num_of_available_table_pointers() != 0:
            ui.removeTableButton.setEnabled(True)

    if root.get_num_of_available_table_pointers() != 0:
        ui.addTableButton.setEnabled(True)
    else:
        ui.addTableButton.setEnabled(False)


def update_tables_text_menu(ui):
    if ui.selected_ow is None and ui.selected_table is not None:
        # A Table was selected
        ui.tableAddressLabel.setText(capitalized_hex(root.tables_list[ui.selected_table].table_pointer_address))
        ui.pointersAddressTableLabel.setText(capitalized_hex(root.tables_list[ui.selected_table].table_address))
        ui.dataAddressTableLabel.setText(capitalized_hex(root.tables_list[ui.selected_table].ow_data_pointers_address))
        ui.framesPointersTableLabel.setText(
            capitalized_hex(root.tables_list[ui.selected_table].frames_pointers_address))
        ui.framesAddressTableLabel.setText(capitalized_hex(root.tables_list[ui.selected_table].frames_address))

    if ui.selected_ow is None and ui.selected_table is None:
        ui.tableAddressLabel.setText("")
        ui.pointersAddressTableLabel.setText("")
        ui.dataAddressTableLabel.setText("")
        ui.framesPointersTableLabel.setText("")
        ui.framesAddressTableLabel.setText("")


def update_palette_info(ui):
    if ui.selected_table is not None:
        ui.paletteIDComboBox.setEnabled(False)
        ui.textColorComboBox.setEnabled(False)
        ui.paletteSlotComboBox.setEnabled(False)

        if ui.selected_ow is not None:
            ui.paletteIDComboBox.setEnabled(True)
            ui.textColorComboBox.setEnabled(True)
            ui.paletteSlotComboBox.setEnabled(True)

            # Sync the Text Color ComboBox
            ow_data_address = root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].ow_data_address
            ui.textColorComboBox.setCurrentIndex(get_text_color(ow_data_address))

            # Sync the Palette Id ComboBox
            id_list = []
            for pal_id in ui.sprite_manager.used_palettes:
                id_list.append(capitalized_hex(pal_id))

            palette_id = get_ow_palette_id(
                root.tables_list[ui.selected_table].ow_data_pointers[ui.selected_ow].ow_data_address)
            index = id_list.index(capitalized_hex(palette_id))
            ui.paletteIDComboBox.setCurrentIndex(index)

            # Sync the Palette Slot Combobox
            ui.paletteSlotComboBox.setCurrentIndex(get_palette_slot(ow_data_address))

            ui.paletteAddressLabel.setText(capitalized_hex(ui.sprite_manager.get_palette_address(palette_id)))
        else:
            ui.paletteAddressLabel.setText("")

        ui.paletteTableAddressLabel.setText(capitalized_hex(ui.sprite_manager.table_address))
        ui.usedPalettesLabel.setText(str(ui.sprite_manager.get_palette_num()))
        ui.availablePalettesLabel.setText(str(ui.sprite_manager.get_free_slots()))


def update_menu_actions(ui):
    ui.menuFrames_Sheet.setEnabled(False)
    ui.menuSpriters_Resource.setEnabled(False)
    ui.actionImport_Frames_Sheet.setEnabled(False)
    ui.actionExport_Frames_Sheet.setEnabled(False)
    ui.actionPaletteCleanup.setEnabled(True)

    if ui.selected_ow is not None:
        ui.menuFrames_Sheet.setEnabled(True)
        ui.menuSpriters_Resource.setEnabled(True)
        ui.actionImport_Frames_Sheet.setEnabled(True)
        ui.actionExport_Frames_Sheet.setEnabled(True)


def update_viewer(ui):
    if ui.selected_ow is not None:
        frame = ui.framesSpinBox.value()
        ui.paint_graphics_view(ui.sprite_manager.get_ow_frame(ui.selected_ow, ui.selected_table, frame))


def update_tree_model(ui):
    ui.statusbar.showMessage("Updating the TreeView...")
    ui.tree_model.resetModel()
    ui.statusbar.showMessage("Ready...")


def update_gui(ui):
    update_ow_menu_buttons(ui)
    update_ow_text_menu(ui)
    update_tables_menu_buttons(ui)
    update_tables_text_menu(ui)
    update_palette_info(ui)
    update_menu_actions(ui)
    ui.OWTreeView.setFocus()
    # update_viewer(ui)
