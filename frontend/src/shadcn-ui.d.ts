// filepath: c:\Project files\Rolsa technologies test\frontend\src\shadcn-ui.d.ts
declare module '@shadcn/ui' {
    import * as React from 'react';
  
    export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
      className?: string;
    }
  
    export const Button: React.FC<ButtonProps>;
  
    export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
      className?: string;
    }
  
    export const Card: React.FC<CardProps>;
  
    export interface TypographyProps extends React.HTMLAttributes<HTMLDivElement> {
      variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body1' | 'body2';
      className?: string;
    }
  
    export const Typography: React.FC<TypographyProps>;
  
    export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
      className?: string;
    }
  
    export const Input: React.FC<InputProps>;
  }