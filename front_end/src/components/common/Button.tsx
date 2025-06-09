import React from 'react';
import './Button.css';

export type ButtonType = 'primary' | 'secondary' | 'tertiary' | 'rag';
export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps {
    type?: 'button' | 'submit' | 'reset';
    buttonType?: ButtonType;
    size?: ButtonSize;
    disabled?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
    className?: string;
    title?: string;
    active?: boolean;
}

const Button:React.FC<ButtonProps> = ({
    type = 'button',
    buttonType = 'primary',
    size = 'medium',
    disabled = false,
    onClick,
    children,
    className,
    title,
    active = false,
}) => {
    const buttonClass = [
        'custom-button', 
        `custom-button--${buttonType}`,
        `custom-button--${size}`,
        active ? 'custom-button--active' : '',
        className,   
    ].filter(Boolean).join(' ');
    return (
        <button
            type={type}
            className={buttonClass}
            onClick = {onClick}
            disabled={disabled}
            title={title}
        >
            {children}
        </button>
    );
}
export default Button;