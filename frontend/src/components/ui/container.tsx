import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"
const containerVariants = cva(
    "container",
    {
        variants: {
        variant: {
            screencenter:
            "w-full flex justify-center items-center min-h-screen h-fit",
        },
        },
        defaultVariants: {
        variant: "screencenter"
        },
    }
)

type VariantPropType = VariantProps<typeof containerVariants>;

const variantElementMap: Record<
    NonNullable<VariantPropType['variant']>,
    string
> = {
    screencenter: 'div',
};

export interface ContainerProps
    extends React.HTMLAttributes<HTMLElement>,
        VariantProps<typeof containerVariants> {
    asChild?: boolean;
    as?: string;
}

const Container = React.forwardRef<HTMLElement, ContainerProps>(
    ({ className, variant, as, asChild, ...props }, ref) => {
        const Comp = asChild
            ? Slot
            : as ?? (variant ? variantElementMap[variant] : undefined) ?? 'div';
        return (
            <Comp
                className={cn(containerVariants({ variant, className }))}
                ref={ref}
                {...props}
            />
        );
    }
);

Container.displayName = 'Container';

export { Container, containerVariants };