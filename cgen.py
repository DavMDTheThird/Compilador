"""
Autores:
    - David Medina Domínguez
        Matricula: A01783155
    - Juan Pablo Cruz Rodríguez
        Matricula: A01783208

Objetivo:
    Creación de una semantica basica para el lenguaje de C-

Instrucciones:
    - tabla(tree, imprime = True)
        o La cual recibe tree, el Árbol Sintáctico Abstracto (AST, por sus siglas en inglés) creado por el parser
        (proyecto 2) y una variable imprime que por default es verdadera (si es verdadera imprime la tabla o 
        tablas de símbolos generadas).
        o Como salida genera la tabla o tablas de símbolos, una por cada bloque.
        
    - semantica(tree, imprime = True)
        o La cual recibe tree, el Árbol Sintáctico Abstracto (AST, por sus siglas en inglés) creado por el parser
        (proyecto 2) y una variable imprime que por default es verdadera. Esta variable la pasa cuando llame a la
        función tabla.
        o Llama a la función tabla y utiliza la tabla o tablas de símbolos que genera.
        o Utiliza reglas lógicas de inferencia para implementar la semántica de C-. Ver descripción de la semántica 
        de C- en el documento en Bb)
"""

global dev3
global symbol_tables
dev3 = False

from semantica import *
from globalTypes import TokenType
from parsingTable import PT

class MIPSGenerator:
    def __init__(self, output_file):
        self.output_file = output_file
        self.current_temp = 0  # For register allocation
        self.current_label = 0  # For unique labels
        self.symbol_tables = None
        self.code = []  # Store generated code
        self.data = []  # Store data section declarations
        self.variables = {}  # Map variable names to stack offsets
        self.arrays = {}  # Map array names to (base_offset, size)
        self.next_var_offset = 0  # Offset from $fp for local variables
        
    def get_new_temp(self):
        """Get next available temporary register"""
        temp = self.current_temp
        self.current_temp = (self.current_temp + 1) % 8  # t0-t7 only
        return f"$t{temp}"
    
    def get_new_label(self):
        """Generate a new unique label"""
        label = f"L{self.current_label}"
        self.current_label += 1
        return label

    def emit(self, instruction):
        """Add an instruction to code section"""
        self.code.append(f"\t{instruction}")

    def emit_data(self, data):
        """Add a declaration to data section"""
        self.data.append(data)

    def allocate_variable(self, var_name, array_size=None):
        """Allocate stack space for a variable or array"""
        if var_name not in self.variables and var_name not in self.arrays:
            if array_size is not None:
                # Allocate array
                size = int(array_size)
                if size <= 0:
                    raise ValueError(f"Invalid array size: {size}")
                
                # Each element takes 4 bytes
                total_size = size * 4
                self.next_var_offset += total_size
                base_offset = -self.next_var_offset
                self.arrays[var_name] = (base_offset, size)
                
                # Initialize array elements to 0
                temp_reg = self.get_new_temp()
                self.emit(f"li {temp_reg}, 0")  # Value to store
                addr_reg = self.get_new_temp()
                self.emit(f"li {addr_reg}, {base_offset}")  # Base address
                self.emit(f"add {addr_reg}, {addr_reg}, $fp")  # Add frame pointer
                
                # Initialize loop counter
                counter_reg = self.get_new_temp()
                self.emit(f"li {counter_reg}, {size}")
                
                # Loop label
                init_label = self.get_new_label()
                self.emit(f"{init_label}:")
                self.emit(f"sw {temp_reg}, ({addr_reg})")  # Store 0
                self.emit(f"addi {addr_reg}, {addr_reg}, 4")  # Next element
                self.emit(f"addi {counter_reg}, {counter_reg}, -1")  # Decrement counter
                self.emit(f"bgtz {counter_reg}, {init_label}")  # Continue if not done
                
                return base_offset
            else:
                # Regular variable
                self.next_var_offset += 4  # Each int takes 4 bytes
                offset = -self.next_var_offset  # Negative offset from $fp
                self.variables[var_name] = offset
                # Initialize variable to 0
                self.emit(f"sw $zero, {offset}($fp)")
                return offset
        return self.variables.get(var_name)

    def get_variable_location(self, var_name):
        """Get the stack location of a variable"""
        # print(f"[DEBUG] Looking up variable location for {var_name}")
        # print(f"[DEBUG] Variables in symbol table: {self.variables}")
        if var_name in self.variables:
            offset = self.variables[var_name]
            # print(f"[DEBUG] Found variable {var_name} at offset {offset}")
            return f"{offset}($fp)"
        # print(f"[DEBUG] Variable {var_name} not found in symbol table")
        return None

    def get_array_element_address(self, array_name, index_reg):
        """Generate code to get the address of an array element"""
        if array_name in self.arrays:
            base_offset, size = self.arrays[array_name]
            # Calculate address: base_offset + (index * 4) + $fp
            temp_reg = self.get_new_temp()
            self.emit(f"# Calculate address for {array_name}[...]")
            self.emit(f"li {temp_reg}, {base_offset}")  # Load base offset
            self.emit(f"mul {index_reg}, {index_reg}, 4")  # Multiply index by 4
            self.emit(f"add {temp_reg}, {temp_reg}, {index_reg}")  # Add to base
            self.emit(f"add {temp_reg}, {temp_reg}, $fp")  # Add frame pointer
            return temp_reg
        return None

    def setup_main(self):
        """Setup the main function's stack frame"""
        self.emit("\n# Setup main's stack frame")
        self.emit("subu $sp, $sp, 4")     # Space for saving $fp
        self.emit("sw $fp, ($sp)")        # Save old $fp
        self.emit("move $fp, $sp")        # Set new frame pointer
        
    def setup_locals(self):
        """Allocate space for local variables"""
        if self.next_var_offset > 0:
            self.emit(f"subu $sp, $sp, {self.next_var_offset}")  # Space for locals

    def cleanup_main(self):
        """Cleanup main's stack frame"""
        self.emit("\n# Cleanup main's stack frame")
        self.emit("move $sp, $fp")      # Restore stack pointer
        self.emit("lw $fp, ($sp)")      # Restore old frame pointer
        self.emit("addu $sp, $sp, 4")   # Pop stack frame

    def write_to_file(self):
        """Write the generated code to output file"""
        with open(self.output_file, 'w') as f:
            # Write data section
            f.write(".data\n")
            f.write("\tnewline: .asciiz \"\\n\"\n")  # For printing newlines
            for data in self.data:
                f.write(f"\t{data}\n")
            
            # Write text section
            f.write("\n.text\n")
            f.write(".globl main\n")
            f.write("main:\n")
            
            # Write the code
            for instruction in self.code:
                f.write(f"{instruction}\n")

    def generate_arithmetic(self, left_reg, op, right_reg):
        """Generate code for basic arithmetic operations"""
        if left_reg and right_reg:  # Only generate if both registers are valid
            dest_reg = self.get_new_temp()
            self.emit(f"\n# Arithmetic operation: {op}")
            if op == '+':
                self.emit(f"add {dest_reg}, {left_reg}, {right_reg}")
            elif op == '-':
                self.emit(f"sub {dest_reg}, {left_reg}, {right_reg}")
            elif op == '*':
                self.emit(f"mul {dest_reg}, {left_reg}, {right_reg}")
            elif op == '/':
                self.emit(f"div {dest_reg}, {left_reg}, {right_reg}")
            return dest_reg
        return None

def find_child_by_symbol(node, symbols):
    """Find a child node by traversing through a list of symbols.
    Args:
        node: The starting node
        symbols: Either a single symbol or a list of symbols to traverse through
    Returns:
        The found node or None if not found
    """
    if not node:
        return None
        
    # If symbols is not a list, treat it as a single symbol (backwards compatibility)
    if not isinstance(symbols, list):
        symbols = [symbols]
    
    current_node = node
    for symbol in symbols:
        if not current_node or not current_node.children:
            return None
            
        # Find child with matching symbol
        found = False
        for child in current_node.children:
            if child.symbol == symbol:
                current_node = child
                found = True
                break
                
        if not found:
            return None
            
    return current_node

def find_terminal_value(node):
    """Helper function to get the terminal value from a node"""
    if node and node.children:
        return node.children[0].symbol
    return None

def traverse_ast(node, generator, phase='declarations'):
    """Traverse the AST and generate code"""
    if not node:
        return

    # Handle program node
    if node.symbol == PT.program:
        if phase == 'declarations':
            # Process declarations first
            dec_list = find_child_by_symbol(node, PT.dec_list)
            if dec_list:
                traverse_ast(dec_list, generator, 'declarations')
        elif phase == 'statements':
            # Find the main function's compound statement
            dec_list = find_child_by_symbol(node, PT.dec_list)
            if dec_list:
                dec = find_child_by_symbol(dec_list, PT.dec)
                if dec:
                    dec_p = find_child_by_symbol(dec, PT.dec_p)
                    if dec_p:
                        compound_stmt = find_child_by_symbol(dec_p, PT.compound_stmt)
                        if compound_stmt:
                            traverse_ast(compound_stmt, generator, 'statements')
        return

    # Handle declaration list
    if node.symbol == PT.dec_list:
        # Process current declaration
        dec = find_child_by_symbol(node, PT.dec)
        if dec:
            traverse_ast(dec, generator, phase)
        
        # Process remaining declarations
        dec_list = find_child_by_symbol(node, PT.dec_list)
        if dec_list:
            traverse_ast(dec_list, generator, phase)
        return

    # Handle declaration
    if node.symbol == PT.dec:
        # Process type specifier
        type_spec = find_child_by_symbol(node, PT.type_specifier)
        if type_spec:
            traverse_ast(type_spec, generator, phase)
        
        # Process ID
        id_node = find_child_by_symbol(node, TokenType.ID)
        if id_node:
            traverse_ast(id_node, generator, phase)
        
        # Process declaration prime
        dec_p = find_child_by_symbol(node, PT.dec_p)
        if dec_p:
            traverse_ast(dec_p, generator, phase)
        return

    # Handle declaration prime
    if node.symbol == PT.dec_p:
        # Process compound statement if present
        compound_stmt = find_child_by_symbol(node, PT.compound_stmt)
        if compound_stmt:
            traverse_ast(compound_stmt, generator, phase)
        return

    # Handle variable declaration
    if node.symbol == PT.var_dec:
        if phase == 'declarations':
            process_variable_declaration(node, generator)
        return

    # Handle compound statement
    if node.symbol == PT.compound_stmt:
        if phase == 'declarations':
            # Process local declarations
            local_decs = find_child_by_symbol(node, PT.local_decs)
            if local_decs:
                traverse_ast(local_decs, generator, phase)
        elif phase == 'statements':
            # Process statement list
            stmt_list = find_child_by_symbol(node, PT.stmt_list)
            if stmt_list:
                process_statement_list(stmt_list, generator)
        return

    # Handle statement list
    if node.symbol == PT.stmt_list:
        process_statement_list(node, generator)
        return

    # Handle local declarations
    if node.symbol == PT.local_decs:
        if phase == 'declarations':
            # Process current declaration
            var_dec = find_child_by_symbol(node, PT.var_dec)
            if var_dec:
                process_variable_declaration(var_dec, generator)
            
            # Process remaining declarations
            local_decs = find_child_by_symbol(node, PT.local_decs)
            if local_decs:
                traverse_ast(local_decs, generator, phase)
        return

    # Handle iteration statement (while loop)
    if node.symbol == PT.iteration_stmt:
        if phase == 'statements':
            # Get the condition expression
            expr = find_child_by_symbol(node, PT.expr)
            if expr:
                # Generate labels for while loop
                start_label = generator.get_new_label()
                end_label = generator.get_new_label()
                
                # Start of while loop
                generator.emit(f"\n{start_label}:")
                
                # Evaluate condition
                condition_reg = handle_expression(expr, generator)
                if condition_reg:
                    # Branch to end if condition is false (0)
                    generator.emit(f"beq {condition_reg}, $zero, {end_label}")
                    
                    # Process the body of the while loop
                    stmt_body = find_child_by_symbol(node, PT.stmt)
                    if stmt_body:
                        # If the body is a compound statement, process it
                        if stmt_body.symbol == PT.compound_stmt:
                            # Process the statement list in the compound statement
                            body_stmt_list = find_child_by_symbol(stmt_body, PT.stmt_list)
                            if body_stmt_list:
                                process_statement_list(body_stmt_list, generator)
                        else:
                            # Handle expression statement
                            expr_stmt = find_child_by_symbol(stmt_body, PT.expr_stmt)
                            if expr_stmt:
                                process_expression_statement(expr_stmt, generator)
                    
                    # Jump back to start of loop
                    generator.emit(f"j {start_label}")
                    
                    # End of while loop
                    generator.emit(f"{end_label}:")
        return

    # Handle expression statement
    if node.symbol == PT.expr_stmt:
        if phase == 'statements':
            process_expression_statement(node, generator)
        return

    # Handle expression
    if node.symbol == PT.expr:
        if phase == 'statements':
            handle_expression(node, generator)
        return

    # Handle term
    if node.symbol == PT.term:
        if phase == 'statements':
            handle_term(node, generator)
        return

    # Handle factor
    if node.symbol == PT.factor:
        if phase == 'statements':
            handle_factor(node, generator)
        return

    # Handle args
    if node.symbol == PT.args:
        if phase == 'statements':
            handle_args(node, generator)
        return

    # Handle array access
    if node.symbol == PT.var:
        if phase == 'statements':
            handle_var(node, generator)
        return

    # Handle lambda pass
    if node.symbol == PT.lambda_pass:
        return

    # Recursively process children
    for child in node.children:
        traverse_ast(child, generator, phase)

def process_statement_list(node, generator):
    """Process a statement list node"""
    if not node:
        return

    # Process current statement
    stmt = find_child_by_symbol(node, PT.stmt)
    if stmt:
        # Handle while statement
        while_stmt = find_child_by_symbol(stmt, PT.iteration_stmt)
        if while_stmt:
            # Get the condition expression
            expr = find_child_by_symbol(while_stmt, PT.expr)
            if expr:
                # Generate labels for while loop
                start_label = generator.get_new_label()
                end_label = generator.get_new_label()
                
                # Start of while loop
                generator.emit(f"\n{start_label}:")
                
                # Evaluate condition
                condition_reg = handle_expression(expr, generator)
                if condition_reg:
                    # Branch to end if condition is false (0)
                    generator.emit(f"beq {condition_reg}, $zero, {end_label}")
                    
                    # Process the body of the while loop
                    stmt_body = find_child_by_symbol(while_stmt, PT.stmt)
                    if stmt_body:
                        # If the body is a compound statement, process it
                        if stmt_body.symbol == PT.compound_stmt:
                            # Process the statement list in the compound statement
                            body_stmt_list = find_child_by_symbol(stmt_body, PT.stmt_list)
                            if body_stmt_list:
                                process_statement_list(body_stmt_list, generator)
                        else:
                            # Handle expression statement
                            expr_stmt = find_child_by_symbol(stmt_body, PT.expr_stmt)
                            if expr_stmt:
                                process_expression_statement(expr_stmt, generator)
                    
                    # Jump back to start of loop
                    generator.emit(f"j {start_label}")
                    
                    # End of while loop
                    generator.emit(f"{end_label}:")
                return
        
        # Handle expression statement
        expr_stmt = find_child_by_symbol(stmt, PT.expr_stmt)
        if expr_stmt:
            process_expression_statement(expr_stmt, generator)

    # Process remaining statements
    stmt_list = find_child_by_symbol(node, PT.stmt_list)
    if stmt_list:
        process_statement_list(stmt_list, generator)

def process_variable_declaration(node, generator):
    """Process a variable declaration node"""
    if not node:
        return

    # Get type specifier
    type_node = find_child_by_symbol(node, PT.type_specifier)
    if not type_node:
        return

    # Get ID
    id_node = find_child_by_symbol(node, TokenType.ID)
    if not id_node:
        return

    var_name = find_terminal_value(id_node)
    if not var_name:
        return

    # Check if this is an array declaration
    var_dec_p = find_child_by_symbol(node, PT.var_dec_p)
    if var_dec_p:
        # Check for array declaration
        if find_child_by_symbol(var_dec_p, "["):
            # Get array size
            num_node = find_child_by_symbol(var_dec_p, TokenType.NUM)
            if num_node:
                array_size = find_terminal_value(num_node)
                generator.allocate_variable(var_name, array_size)
        # Check for semicolon (regular variable)
        elif find_child_by_symbol(var_dec_p, ";"):
            generator.allocate_variable(var_name)
        # Check for more variable declarations
        elif find_child_by_symbol(var_dec_p, ","):
            # Regular variable
            generator.allocate_variable(var_name)
            # Process next variable
            next_id = find_child_by_symbol(var_dec_p, TokenType.ID)
            if next_id:
                next_var_name = find_terminal_value(next_id)
                if next_var_name:
                    generator.allocate_variable(next_var_name)
                    # Check for more variables
                    next_var_dec_p = find_child_by_symbol(var_dec_p, PT.var_dec_p)
                    if next_var_dec_p:
                        next_id = find_child_by_symbol(next_var_dec_p, TokenType.ID)
                        if next_id:
                            next_var_name = find_terminal_value(next_id)
                            if next_var_name:
                                generator.allocate_variable(next_var_name)
    else:
        # Regular variable
        generator.allocate_variable(var_name)

def process_local_declarations(node, generator):
    """Process local declarations"""
    if not node:
        return

    # Process current declaration
    var_dec = find_child_by_symbol(node, PT.var_dec)
    if var_dec:
        process_variable_declaration(var_dec, generator)

    # Process remaining declarations
    local_decs = find_child_by_symbol(node, PT.local_decs)
    if local_decs:
        process_local_declarations(local_decs, generator)

def process_expression_statement(node, generator):
    """Process an expression statement node"""
    if not node:
        return

    expr = find_child_by_symbol(node, PT.expr)
    if not expr:
        return

    # Get the ID for assignment (traversing through simple_expr -> additive_expr -> term -> factor -> ID)
    simple_expr = find_child_by_symbol(expr, PT.simple_expr)
    if simple_expr:
        additive_expr = find_child_by_symbol(simple_expr, PT.additive_expr)
        if additive_expr:
            term = find_child_by_symbol(additive_expr, PT.term)
            if term:
                factor = find_child_by_symbol(term, PT.factor)
                if factor:
                    id_node = find_child_by_symbol(factor, TokenType.ID)
                    if id_node:
                        var_name = find_terminal_value(id_node)
                        if var_name == "output":
                            # Handle output() call
                            factor_p = find_child_by_symbol(factor, PT.factor_p)
                            if factor_p and find_child_by_symbol(factor_p, "("):
                                args = find_child_by_symbol(factor_p, PT.args)
                                if args:
                                    arg_list = find_child_by_symbol(args, PT.arg_list)
                                    if arg_list:
                                        arg_expr = find_child_by_symbol(arg_list, PT.expr)
                                        if arg_expr:
                                            arg_reg = handle_expression(arg_expr, generator)
                                            if arg_reg:
                                                # Print the value
                                                generator.emit(f"move $a0, {arg_reg}")
                                                generator.emit("li $v0, 1")  # syscall 1 prints integer
                                                generator.emit("syscall")
                                                # Print newline
                                                generator.emit("li $v0, 4")  # syscall 4 prints string
                                                generator.emit("la $a0, newline")
                                                generator.emit("syscall")
                            return
                
    expr_p = find_child_by_symbol(expr, PT.expr_p)
    if expr_p:
        assign_op = find_child_by_symbol(expr_p, '=')
        if assign_op:
            # Get the right side of the assignment
            rhs_expr = find_child_by_symbol(expr_p, PT.expr)
            if rhs_expr:
                # Check if it's an input() call
                func_id = find_child_by_symbol(rhs_expr, [PT.simple_expr, PT.additive_expr, PT.term, PT.factor, TokenType.ID])
                if func_id:
                    func_name = find_terminal_value(func_id)
                    if func_name == "input":
                        # Check if this is an array assignment
                        var_p = find_child_by_symbol(factor, PT.var_p)
                        if var_p and find_child_by_symbol(var_p, "["):
                            # Get index expression
                            expr_node = find_child_by_symbol(var_p, PT.expr)
                            if expr_node:
                                # Evaluate index expression
                                index_reg = handle_expression(expr_node, generator)
                                if index_reg:
                                    # Get array element address
                                    addr_reg = generator.get_array_element_address(var_name, index_reg)
                                    if addr_reg:
                                        # Generate input code
                                        generator.emit("\n# Reading input into array element")
                                        generator.emit("li $v0, 5")  # syscall 5 reads an integer
                                        generator.emit("syscall")
                                        generator.emit(f"sw $v0, ({addr_reg})")  # Store input directly
                                        return
                        else:
                            # Regular variable input
                            generator.emit("\n# Reading input from user")
                            generator.emit("li $v0, 5")  # syscall 5 reads an integer
                            generator.emit("syscall")
                            var_loc = generator.get_variable_location(var_name)
                            if var_loc:
                                generator.emit(f"sw $v0, {var_loc}")  # Store input directly
                            return
                
                # Not an input() call, handle as regular expression
                # Check if this is an array assignment
                var_p = find_child_by_symbol(factor, PT.var_p)
                if var_p and find_child_by_symbol(var_p, "["):
                    # Get index expression
                    expr_node = find_child_by_symbol(var_p, PT.expr)
                    if expr_node:
                        # Evaluate index expression
                        index_reg = handle_expression(expr_node, generator)
                        if index_reg:
                            # Get array element address
                            addr_reg = generator.get_array_element_address(var_name, index_reg)
                            if addr_reg:
                                # Evaluate right-hand side
                                result_reg = handle_expression(rhs_expr, generator)
                                if result_reg:
                                    generator.emit(f"sw {result_reg}, ({addr_reg})")
                                    return
                else:
                    # Regular variable assignment
                    result_reg = handle_expression(rhs_expr, generator)
                    if result_reg:
                        var_loc = generator.get_variable_location(var_name)
                        if var_loc:
                            generator.emit(f"sw {result_reg}, {var_loc}")
                            return

        # Not an assignment, handle as regular expression
        handle_expression(expr, generator)

def handle_expression(node, generator):
    """Handle expression nodes"""
    if not node:
        return None

    # Handle simple expression first
    simple_expr = find_child_by_symbol(node, PT.simple_expr)
    if simple_expr:
        # Check for comparison operation
        simple_expr_p = find_child_by_symbol(simple_expr, PT.simple_expr_p)
        if simple_expr_p:
            # Get left side
            left_reg = handle_additive_expression(find_child_by_symbol(simple_expr, PT.additive_expr), generator)
            if left_reg:
                # Get comparison operator
                relop = find_child_by_symbol(simple_expr_p, PT.relop)
                if relop:
                    op = find_terminal_value(relop)
                    # Get right side
                    right_additive = find_child_by_symbol(simple_expr_p, PT.additive_expr)
                    if right_additive:
                        right_reg = handle_additive_expression(right_additive, generator)
                        if right_reg:
                            # Generate comparison code
                            result_reg = generator.get_new_temp()
                            if op == '<':
                                generator.emit(f"slt {result_reg}, {left_reg}, {right_reg}")
                            elif op == '<=':
                                generator.emit(f"slt {result_reg}, {right_reg}, {left_reg}")
                                generator.emit(f"xori {result_reg}, {result_reg}, 1")
                            elif op == '>':
                                generator.emit(f"slt {result_reg}, {right_reg}, {left_reg}")
                            elif op == '>=':
                                generator.emit(f"slt {result_reg}, {left_reg}, {right_reg}")
                                generator.emit(f"xori {result_reg}, {result_reg}, 1")
                            elif op == '==':
                                generator.emit(f"sub {result_reg}, {left_reg}, {right_reg}")
                                generator.emit(f"sltiu {result_reg}, {result_reg}, 1")
                            elif op == '!=':
                                generator.emit(f"sub {result_reg}, {left_reg}, {right_reg}")
                                generator.emit(f"sltu {result_reg}, $zero, {result_reg}")
                            return result_reg
        return handle_additive_expression(find_child_by_symbol(simple_expr, PT.additive_expr), generator)

    return None

def handle_additive_expression(node, generator):
    """Handle additive expression nodes"""
    if not node:
        return None

    # Get initial term
    term = find_child_by_symbol(node, PT.term)
    if not term:
        return None
    
    result_reg = handle_term(term, generator)
    if not result_reg:
        return None

    # Check for addition/subtraction
    additive_expr_p = find_child_by_symbol(node, PT.additive_expr_p)
    while additive_expr_p:
        # Get operator and next term in one traversal
        addop = find_child_by_symbol(additive_expr_p, PT.addop)
        term = find_child_by_symbol(additive_expr_p, PT.term)
        
        if addop and term:
            op = find_terminal_value(addop)
            right_reg = handle_term(term, generator)
            if right_reg:
                result_reg = generator.generate_arithmetic(result_reg, op, right_reg)
        
        # Move to next operation if any
        additive_expr_p = find_child_by_symbol(additive_expr_p, PT.additive_expr_p)
        if additive_expr_p and find_child_by_symbol(additive_expr_p, PT.lambda_pass):
            break

    return result_reg

def handle_term(node, generator):
    """Handle term nodes"""
    if not node:
        return None

    # Get initial factor
    factor = find_child_by_symbol(node, PT.factor)
    if not factor:
        return None
    
    result_reg = handle_factor(factor, generator)
    if not result_reg:
        return None

    # Check for multiplication/division
    term_p = find_child_by_symbol(node, PT.term_p)
    while term_p:
        # Get operator and next factor in one traversal
        mulop = find_child_by_symbol(term_p, PT.mulop)
        factor = find_child_by_symbol(term_p, PT.factor)
        
        if mulop and factor:
            op = find_terminal_value(mulop)
            right_reg = handle_factor(factor, generator)
            if right_reg:
                result_reg = generator.generate_arithmetic(result_reg, op, right_reg)
        
        # Move to next operation if any
        term_p = find_child_by_symbol(term_p, PT.term_p)
        if term_p and find_child_by_symbol(term_p, PT.lambda_pass):
            break

    return result_reg

def handle_factor(node, generator):
    """Handle factor nodes"""
    if not node:
        return None

    # Handle ID (variable)
    id_node = find_child_by_symbol(node, TokenType.ID)
    if id_node:
        var_name = find_terminal_value(id_node)
        if var_name:
            # Check if this is an array access
            var_p = find_child_by_symbol(node, PT.var_p)
            if var_p and find_child_by_symbol(var_p, "["):
                # Get index expression
                expr_node = find_child_by_symbol(var_p, PT.expr)
                if expr_node:
                    # Evaluate index expression
                    index_reg = handle_expression(expr_node, generator)
                    if index_reg:
                        # Get array element address
                        addr_reg = generator.get_array_element_address(var_name, index_reg)
                        if addr_reg:
                            # Load value from array
                            result_reg = generator.get_new_temp()
                            generator.emit(f"lw {result_reg}, ({addr_reg})")
                            return result_reg
            else:
                # Regular variable access
                var_loc = generator.get_variable_location(var_name)
                if var_loc:
                    result_reg = generator.get_new_temp()
                    generator.emit(f"\n# Loading {var_name}")
                    generator.emit(f"lw {result_reg}, {var_loc}")
                    return result_reg

    # Handle NUM
    num_node = find_child_by_symbol(node, TokenType.NUM)
    if num_node:
        value = find_terminal_value(num_node)
        if value:
            result_reg = generator.get_new_temp()
            generator.emit(f"\n# Loading constant {value}")
            generator.emit(f"li {result_reg}, {value}")
            return result_reg

    return None

def codeGen(tree, output_file):
    # Run semantic analysis first to get symbol tables
    symbol_tables = semantica(tree, False)
    
    # Initialize code generator
    generator = MIPSGenerator(output_file)
    generator.symbol_tables = symbol_tables
    
    # Setup main's stack frame
    generator.setup_main()
    
    # Process declarations first
    traverse_ast(tree[0], generator, "declarations")
    
    # Setup space for local variables
    generator.setup_locals()
    
    # Process statements
    traverse_ast(tree[0], generator, "statements")
    
    # Cleanup main's stack frame
    generator.cleanup_main()
    
    # Exit program
    generator.emit("\n# Exit program")
    generator.emit("li $v0, 10")
    generator.emit("syscall")
    
    # Write generated code to file
    generator.write_to_file()

def globales(prog, pos, long, line_ = 0):
    global programa, posicion, progLong, line, symbol_tables
    programa = prog
    posicion = pos
    progLong = long
    line = line_
    globalesSemantica(prog, pos, long, line)