import { cn } from "../../utils";
import React from "react";
import { Loader } from "lucide-react"; 

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "default" | "outline" | "ghost" | "submit";
    isLoading?: boolean;
    icon?: React.ReactNode; 
}

export const Button = ({ className, variant = "default", isLoading, icon, children, ...props }: ButtonProps) => {
    const baseStyle = "px-4 py-2 rounded font-semibold transition-colors flex items-center justify-center gap-2";
    const variants = {
        default: "bg-gray-800 text-white hover:bg-blue-700", 
        outline: "border border-gray-600 text-blue-600 hover:bg-blue-100", 
        ghost: "text-blue-600 hover:bg-blue-50",
        submit: "bg-black text-white hover:bg-gray-900" 
    };

    return (
        <button
            className={cn(baseStyle, variants[variant], className, isLoading && "opacity-70 cursor-not-allowed")}
            disabled={isLoading || props.disabled} 
            {...props}
        >
            {isLoading && <Loader className="animate-spin h-5 w-5" />}
            {icon && !isLoading && <span>{icon}</span>}
            <span>{children}</span> 
        </button>
    );
};