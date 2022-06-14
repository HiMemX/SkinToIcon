import helpers

def get_face(skin):
    return helpers.get_matrix_section(skin, 8, 8, 8, 8)

def get_face_mask(skin):
    return helpers.get_matrix_section(skin, 40, 8, 8, 8)
    